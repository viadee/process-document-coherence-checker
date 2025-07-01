import os
import xml.etree.ElementTree as ET

class BPMNPreprocessing:
    def __init__(self, directory):
        """Initialize the preprocessor with the directory of BPMN files."""
        self.directory = directory
        self.modified_directory = os.path.join(directory, "modified")
        self.setup_directory()
        self.register_namespaces()

    def setup_directory(self):
        """Ensure the directory for modified files exists."""
        if not os.path.exists(self.modified_directory):
            os.makedirs(self.modified_directory)

    def register_namespaces(self):
        """Register namespaces to maintain XML structure and prefixes."""
        namespaces = {
            'http://www.omg.org/spec/BPMN/20100524/MODEL': 'bpmn',
            'http://www.omg.org/spec/BPMN/20100524/DI': 'bpmndi',
            'http://www.omg.org/spec/DD/20100524/DC': 'dc',
            'http://www.omg.org/spec/DD/20100524/DI': 'di',
        }
        for uri, prefix in namespaces.items():
            ET.register_namespace(prefix, uri)

    def preprocess_files(self, file_paths):
        """Preprocess only selected files to remove visual elements."""
        modified_files = []
        for file_path in file_paths:
            # Parse the BPMN file
            tree = ET.parse(file_path)
            root = tree.getroot()
            # Remove visual components from the BPMN
            self.remove_visual_elements(root)
            # Save changes and keep track of the new file path
            modified_file = self.save_modified_file(tree, os.path.basename(file_path))
            modified_files.append(modified_file)
        return modified_files

    def remove_visual_elements(self, root):
        """Remove visual elements to focus on the process structure."""
        for diagram in root.findall('{http://www.omg.org/spec/BPMN/20100524/DI}BPMNDiagram'):
            root.remove(diagram)

    def save_modified_file(self, tree, filename):
        """Save the modified XML tree to a new file in the modified directory."""
        modified_file_path = os.path.join(self.modified_directory, filename[:-5] + "_shortened.bpmn")
        tree.write(modified_file_path, xml_declaration=True, encoding='utf-8')
        return modified_file_path