#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

# 添加src目录到Python路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

try:
    print("Testing imports...")
    
    from PyQt5.QtWidgets import QDialog, QApplication
    print("✅ PyQt5 imports successful")
    
    # Create a minimal QApplication for testing
    app = QApplication([])
    
    # Test importing the dialogs module
    import ui.dialogs
    print("✅ ui.dialogs module imported")
    
    # Check what's in the module
    print("Module contents:", dir(ui.dialogs))
    
    # Try to import the classes
    from ui.dialogs import ChatDialog
    print("✅ ChatDialog imported successfully")
    
    from ui.dialogs import TaskDialog
    print("✅ TaskDialog imported successfully")
    
    from ui.dialogs import TravelDialog
    print("✅ TravelDialog imported successfully")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()