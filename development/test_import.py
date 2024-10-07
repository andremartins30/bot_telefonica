import sys
print(sys.executable)
print(sys.path)

try:
    from selenium import webdriver
    print("Selenium imported successfully")
except ImportError as e:
    print(f"Failed to import Selenium: {e}")

import site
print("\nSite packages:")
print(site.getsitepackages())