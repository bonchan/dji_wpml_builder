import zipfile
import os
from pathlib import Path
from .utils.xml_builder import build_template_xml, build_waylines_xml
from dji_wpml.models.mission_information import MissionInformation

class KMZGenerator:
    def __init__(self, mission_information: MissionInformation):
        self.mission_information = mission_information

    def build(self, output_filename: str, output_dir: str = ".", verify: bool = False, unzip: bool = False):
        """
        Builds the KMZ file.
        :param output_filename: Name of the file (e.g., 'mission.kmz')
        :param output_dir: Target directory. Defaults to current directory ('.')
        :param verify: If True, prints a console check of the content.
        :param unzip: If True, extracts the files to a folder for manual inspection.
        """
        # 1. Handle Paths
        target_dir = Path(output_dir)
        target_dir.mkdir(parents=True, exist_ok=True) 
        full_path = target_dir / output_filename

        # 2. Generate XMLs
        template_xml = build_template_xml(self.mission_information)
        waylines_xml = build_waylines_xml(self.mission_information)
        
        # 3. Create the KMZ
        with zipfile.ZipFile(full_path, 'w', zipfile.ZIP_DEFLATED) as kmz:
            kmz.writestr('wpmz/template.kml', template_xml)
            kmz.writestr('wpmz/waylines.wpml', waylines_xml)
            
        print(f"✅ KMZ generated at: {full_path}")

        if verify:
            self._verify_kmz(full_path)
        
        if unzip:
            self._unzip_kmz(full_path)
            
        return full_path

    def _verify_kmz(self, kmz_path):
        """Quick console check of the generated XML content."""
        print(f"--- Verifying {os.path.basename(kmz_path)} ---")
        try:
            with zipfile.ZipFile(kmz_path, 'r') as kmz:
                content = kmz.read('wpmz/template.kml').decode('utf-8')
                if "<Placemark>" in content:
                    print("   ✓ Success: Waypoints found in XML.")
                else:
                    print("   ⚠ Error: XML is empty of waypoints! Check your Jinja2 loops.")
        except Exception as e:
            print(f"   ✗ Verification failed: {e}")

    def _unzip_kmz(self, kmz_path):
        """Physically extracts the KMZ to a folder for manual code review."""
        kmz_path = Path(kmz_path)
        target_dir = kmz_path.parent
        
        # Create a folder name by removing .kmz extension
        extract_dir = target_dir / f"{kmz_path.stem}_extracted"
        extract_dir.mkdir(exist_ok=True)
        
        with zipfile.ZipFile(kmz_path, 'r') as kmz_ref:
            kmz_ref.extractall(extract_dir)
        
        print(f"📂 Contents extracted to: {extract_dir}")
        print(f"   - Inspect: {extract_dir}/wpmz/template.kml")
        print(f"   - Inspect: {extract_dir}/wpmz/waylines.wpml")