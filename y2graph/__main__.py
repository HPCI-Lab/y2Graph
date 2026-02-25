import uuid
import yaml
from prov.model import ProvDocument
from y2graph.utils import custom_prov_to_dot, replace_nodes_with_images
import argparse
import os
import subprocess
import json as _json

IDENTIFIER = "y2Graph"

# Namespace used for identifiers that are shared across files (e.g. "Training",
# "startedAtTime", "gabrielepadovani"). These live under a stable URI so they
# unify correctly when multiple documents are merged.
SHARED_NS = "shared"
SHARED_URI = "shared"


class ProvWorkflowManager:
    def __init__(self):
        self.doc = ProvDocument()
        self.doc.add_namespace(IDENTIFIER, IDENTIFIER)
        self.doc.add_namespace(SHARED_NS, SHARED_URI)
        self.entities = {}
        self.activities = {}

    def _get_or_create_entity(self, uid, ents, label=None):
        if not uid:
            uid = f"{IDENTIFIER}:entity-{uuid.uuid4()}"

        if uid not in self.entities:
            self.entities[uid] = self.doc.entity(
                uid, {"prov:label": label or uid}
            )

        if ents:
            name = uid.replace(f"{IDENTIFIER}:", "")
            if name in ents:
                self.entities[uid].add_attributes(
                    {"prov:" + k: v for k, v in ents[name].items()}
                )

        return self.entities[uid]

    def _create_activity(self, aid=None, label=None, attributes=None):
        if attributes is None:
            attributes = {}
        if not aid:
            aid = f"activity-{uuid.uuid4()}"
        attributes["prov:label"] = label or aid
        activity = self.doc.activity(aid, None, None, attributes)
        self.activities[aid] = activity
        return activity

    def _create_user(self, label):
        return self.doc.agent(label)

    def load_from_yaml(self, yaml_path):
        with open(yaml_path, "r") as f:
            workflow = yaml.safe_load(f)

        entities = workflow.get("entities", {})

        for task in workflow.get("tasks", []):
            task_id = task.get("id") or f"activity-{uuid.uuid4()}"
            task_id = f"{IDENTIFIER}:{task_id}"

            label = task.get("label", task_id)
            agent = task.get("agent")
            attributes = task.get("attributes", [])

            attrs = {
                f"{IDENTIFIER}:{list(a.keys())[0]}": list(a.values())[0]
                for a in attributes
            }

            inputs = [f"{IDENTIFIER}:{i}" for i in task.get("inputs", []) if i]
            outputs = [f"{IDENTIFIER}:{o}" for o in task.get("outputs", []) if o]

            activity = self._create_activity(task_id, label, attrs)
            if agent: 
                user_id = IDENTIFIER + ":" + agent
                user = self._create_user(user_id)
                activity.wasAssociatedWith(user)

            if agent:
                user_id = f"{IDENTIFIER}:{agent}"
                user = self._create_user(user_id)
                activity.wasAssociatedWith(user)

            for input_id in inputs:
                entity = self._get_or_create_entity(input_id, entities)
                self.doc.used(activity, entity)

            for output_id in outputs:
                entity = self._get_or_create_entity(output_id, entities)
                self.doc.wasGeneratedBy(entity, activity)

    def export_prov_json(self, path):
        with open(path, "w") as f:
            f.write(self.doc.serialize(indent=2))

    def render_graph(self, path, direction="BT", show_element_attributes=True):
        dot = custom_prov_to_dot(self.doc, direction=direction, show_element_attributes=show_element_attributes)
        dot_str = replace_nodes_with_images(dot.to_string())

        dot_path = os.path.splitext(path)[0] + ".dot"
        with open(dot_path, "w") as f:
            f.write(dot_str)

        if path.endswith(".pdf"):
            subprocess.run(["dot", "-Tpdf", dot_path, "-o", path])
        else:
            subprocess.run(["dot", "-Tpng", dot_path, "-o", path])

    def load_from_prov_json(self, json_path):
        """
        Load an existing PROV-JSON and merge it into the current document.

        Problem: each file uses "default" as a namespace prefix but points it to a
        different, file-specific URI (e.g. "test_prov_experiment_GR0_8"). Identifiers
        like "Training", "startedAtTime", "gabrielepadovani" are all bare names in the
        default namespace, so across files they resolve to different URIs and never unify.

        Solution: parse the JSON manually and rewrite identifiers before deserializing:
          - Identifiers that are file-specific (same name as the default URI, or
            contain it as a path component like "std.time/test_prov_experiment_GR0_8")
            get scoped to their own namespace: <default_uri>:<identifier>
          - Everything else goes into the stable SHARED_NS namespace so it unifies
            across all files.
        """
        with open(json_path, "r", encoding="utf-8") as f:
            data = _json.load(f)

        prefix_map = data.get("prefix", {})
        default_uri = prefix_map.get("default", None)

        if default_uri is None:
            # No default namespace conflict — load normally
            temp_doc = ProvDocument()
            with open(json_path, "rb") as f2:
                temp_doc = temp_doc.deserialize(content=f2.read())
            for ns in temp_doc.namespaces:
                if ns.prefix not in self.doc._namespaces:
                    self.doc.add_namespace(ns.prefix, str(ns.uri))
            self.doc.update(temp_doc)
            return

        def is_file_specific(identifier: str) -> bool:
            """
            Returns True if this identifier is specific to this file
            (i.e. it IS the experiment name, or contains it as a path segment).
            """
            return (
                identifier == default_uri
                or ("/" + default_uri) in identifier
                or (default_uri + "/") in identifier
            )

        def rewrite_id(identifier: str) -> str:
            """Route identifier to either the file-specific or shared namespace."""
            if is_file_specific(identifier):
                return f"{default_uri}:{identifier}"
            return f"{SHARED_NS}:{identifier}"

        def rewrite_ref(ref: str) -> str:
            """Rewrite a reference value that may be bare, prefixed, or a blank node."""
            if ref.startswith("_:"):
                return ref  # blank node — unchanged
            if ":" in ref:
                return ref  # already has an explicit prefix — unchanged
            return rewrite_id(ref)

        # Register namespaces in the main document
        if default_uri not in self.doc._namespaces:
            self.doc.add_namespace(default_uri, default_uri)
        for pfx, uri in prefix_map.items():
            if pfx != "default" and pfx not in self.doc._namespaces:
                self.doc.add_namespace(pfx, uri)

        # Build rewritten document
        new_data: dict = {"prefix": {}}

        # Replace the file-specific "default" entry with two stable namespaces
        for pfx, uri in prefix_map.items():
            if pfx == "default":
                new_data["prefix"][default_uri] = default_uri
                new_data["prefix"][SHARED_NS] = SHARED_URI
            else:
                new_data["prefix"][pfx] = uri

        # Rewrite element sections (entity, activity, agent) — top-level keys are identifiers
        for section in ("entity", "activity", "agent"):
            if section not in data:
                continue
            new_data[section] = {}
            for key, val in data[section].items():
                new_data[section][rewrite_id(key)] = val

        # Relation types and the fields that hold identifier references
        relation_field_map = {
            "wasGeneratedBy":    ["prov:entity", "prov:activity"],
            "used":              ["prov:activity", "prov:entity"],
            "wasAssociatedWith": ["prov:activity", "prov:agent"],
            "wasInformedBy":     ["prov:informed", "prov:informant"],
            "wasDerivedFrom":    ["prov:generatedEntity", "prov:usedEntity"],
            "wasAttributedTo":   ["prov:entity", "prov:agent"],
            "actedOnBehalfOf":   ["prov:delegate", "prov:responsible"],
            "wasStartedBy":      ["prov:activity", "prov:trigger"],
            "wasEndedBy":        ["prov:activity", "prov:trigger"],
            "hadMember":         ["prov:collection", "prov:entity"],
            "wasInvalidatedBy":  ["prov:entity", "prov:activity"],
        }

        for rel_type, ref_fields in relation_field_map.items():
            if rel_type not in data:
                continue
            new_data[rel_type] = {}
            for blank_id, record in data[rel_type].items():
                new_record = {}
                for field, value in record.items():
                    if field in ref_fields and isinstance(value, str):
                        new_record[field] = rewrite_ref(value)
                    else:
                        new_record[field] = value
                new_data[rel_type][blank_id] = new_record

        # Deserialize the rewritten JSON and merge into the main document
        rewritten_json = _json.dumps(new_data).encode("utf-8")
        temp_doc = ProvDocument()
        temp_doc = temp_doc.deserialize(content=rewritten_json)
        self.doc.update(temp_doc)

    def deduplicate_relations(self):
        """
        Remove duplicate PROV relation records (used, wasGeneratedBy, etc.).
        Keeps one instance per unique signature.
        """
        seen = set()
        unique_records = []

        for record in self.doc.get_records():
            if record.is_relation():
                sig = (
                    record.get_type(),
                    tuple(record.args),
                    tuple(record.attributes),
                )
                if sig in seen:
                    continue
                seen.add(sig)

            unique_records.append(record)

        self.doc._records = unique_records


def main():
    parser = argparse.ArgumentParser(
        prog="y2graph",
        description="Build and merge W3C-PROV provenance graphs from YAML or PROV-JSON.",
    )

    parser.add_argument(
        "filenames",
        nargs="+",
        help="Input files (YAML workflows or PROV JSONs)",
    )

    parser.add_argument(
        "--from-json",
        action="store_true",
        help="Treat input files as PROV-JSON instead of YAML",
    )

    parser.add_argument(
        "--join",
        action="store_true",
        help="Join all inputs into a single PROV document",
    )

    parser.add_argument("-j", "--json", help="Output JSON filename")
    parser.add_argument("-o", "--output", help="Output graph filename")
    parser.add_argument("-p", "--pdf", default="True", help="Output to pdf file")
    parser.add_argument("-d", "--direction", default="RL", help="Direction in which the nodes will be displayed")
    parser.add_argument("-l", "--labels", default=True, help="If node labels will be displayed or not")

    args = parser.parse_args()

    IMG_EXT = ".pdf" if args.pdf == "True" else ".png"

    # =========================
    # JOINED MODE
    # =========================
    if args.join:
        manager = ProvWorkflowManager()

        for file in args.filenames:
            if args.from_json:
                manager.load_from_prov_json(file)
            else:
                manager.load_from_yaml(file)

        json_path = args.json or "final_prov.json"
        if not json_path.endswith(".json"):
            json_path += ".json"

        graph_path = args.output or "final_graph.pdf"
        if not graph_path.endswith(IMG_EXT):
            graph_path += IMG_EXT

        manager.deduplicate_relations()
        # if not args.from_json:
        manager.export_prov_json(json_path)
        manager.render_graph(graph_path, direction=args.direction, show_element_attributes=args.labels)

    # =========================
    # SEPARATE MODE
    # =========================
    else:
        for file in args.filenames:
            manager = ProvWorkflowManager()

            if args.from_json:
                manager.load_from_prov_json(file)
            else:
                manager.load_from_yaml(file)

            base = os.path.splitext(os.path.basename(file))[0]
            manager.deduplicate_relations()
            if not args.from_json:
                manager.export_prov_json(f"{base}.json")
            manager.render_graph(f"{base}{IMG_EXT}", direction=args.direction, show_element_attributes=args.labels)

if __name__ == "__main__":
    main()