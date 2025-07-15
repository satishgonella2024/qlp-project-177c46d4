from models import VersionResponse
import platform

def health_check():
    return {"status": "OK"}

def get_version():
    return {
        "version": "1.0.0",
        "python_version": platform.python_version(),
        "platform": platform.platform()
    }