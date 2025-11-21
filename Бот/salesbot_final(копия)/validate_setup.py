#!/usr/bin/env python3
"""
Salesbot Setup Validation Script
Run this script to verify that all components are properly configured
"""
import sys
import os

def check_environment():
    """Check required environment variables"""
    print("=" * 60)
    print("Checking Environment Variables")
    print("=" * 60)
    
    required = {
        'TELEGRAM_TOKEN': ['TELEGRAM_TOKEN', 'TELEGRAM_BOT_TOKEN', 'TG_BOT_TOKEN'],
        'DEEPSEEK_API_KEY': ['DEEPSEEK_API_KEY'],
    }
    
    optional = {
        'DEEPSEEK_MODEL': ['DEEPSEEK_MODEL'],
        'ADMIN_CHAT_ID': ['ADMIN_CHAT_ID'],
        'VOICE_API_KEY': ['VOICE_API_KEY'],
    }
    
    all_ok = True
    
    for name, vars in required.items():
        found = False
        for var in vars:
            if os.getenv(var):
                print(f"✅ {name}: Set (via {var})")
                found = True
                break
        if not found:
            print(f"❌ {name}: Not set (tried: {', '.join(vars)})")
            all_ok = False
    
    for name, vars in optional.items():
        found = False
        for var in vars:
            if os.getenv(var):
                print(f"✅ {name}: Set (via {var})")
                found = True
                break
        if not found:
            print(f"⚠️  {name}: Not set (optional)")
    
    return all_ok

def check_dependencies():
    """Check required Python packages"""
    print("\n" + "=" * 60)
    print("Checking Python Dependencies")
    print("=" * 60)
    
    required_packages = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('aiogram', 'Aiogram'),
        ('requests', 'Requests'),
        ('pydantic', 'Pydantic'),
    ]
    
    all_ok = True
    
    for package, name in required_packages:
        try:
            __import__(package)
            # Get version if available
            try:
                mod = __import__(package)
                version = getattr(mod, '__version__', 'unknown')
                print(f"✅ {name}: {version}")
            except:
                print(f"✅ {name}: installed")
        except ImportError:
            print(f"❌ {name}: Not installed")
            all_ok = False
    
    # Check aiogram version
    try:
        import aiogram
        version = aiogram.__version__
        major_version = int(version.split('.')[0])
        if major_version >= 3:
            print(f"✅ Aiogram version check: {version} (>=3.0 required)")
        else:
            print(f"❌ Aiogram version check: {version} (>=3.0 required)")
            all_ok = False
    except:
        pass
    
    return all_ok

def check_modules():
    """Check that all training modules can be imported"""
    print("\n" + "=" * 60)
    print("Checking Training Modules")
    print("=" * 60)
    
    modules = [
        ('modules.master_path.v3.engine', 'MasterPath'),
        ('modules.arena.v4.engine', 'ArenaEngine'),
        ('modules.objections.v3.engine', 'ObjectionEngine'),
        ('modules.upsell.v3.engine', 'UpsellEngine'),
        ('modules.deepseek_persona.v1.service', 'DeepSeek Persona'),
    ]
    
    all_ok = True
    
    for module_path, name in modules:
        try:
            import importlib
            importlib.import_module(module_path)
            print(f"✅ {name}: Available")
        except Exception as e:
            print(f"❌ {name}: Failed to load - {e}")
            all_ok = False
    
    return all_ok

def check_telegram_handlers():
    """Check that telegram handlers are registered"""
    print("\n" + "=" * 60)
    print("Checking Telegram Handler Registration")
    print("=" * 60)
    
    # Set dummy token if not set
    if not os.getenv('TELEGRAM_TOKEN'):
        os.environ['TELEGRAM_TOKEN'] = '123456789:ABCdefGHIjklMNOpqrsTUVwxyz'
    
    try:
        from telegram_bot import dp
        
        # Count handlers
        handler_count = 0
        for router in [dp] + list(dp.sub_routers):
            handler_count += len(router.message.handlers)
        
        if handler_count > 0:
            print(f"✅ Telegram handlers registered: {handler_count} handlers")
            return True
        else:
            print(f"⚠️  No telegram handlers found (this may be normal if they're in sub-routers)")
            return True
    except Exception as e:
        print(f"❌ Failed to check telegram handlers: {e}")
        return False

def check_fastapi():
    """Check that FastAPI app can be created"""
    print("\n" + "=" * 60)
    print("Checking FastAPI Application")
    print("=" * 60)
    
    try:
        from startup import app
        
        # Count routes
        route_count = len([r for r in app.routes if hasattr(r, 'path')])
        print(f"✅ FastAPI app created: {route_count} routes")
        
        # Check key routes
        routes = [r.path for r in app.routes if hasattr(r, 'path')]
        key_routes = ['/api/public/v1/health', '/api/public/v1/routes_summary']
        
        for route in key_routes:
            if route in routes:
                print(f"✅ Key route exists: {route}")
            else:
                print(f"⚠️  Key route missing: {route}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to create FastAPI app: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all validation checks"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 12 + "SALESBOT SETUP VALIDATION" + " " * 21 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    results = {
        'Environment Variables': check_environment(),
        'Python Dependencies': check_dependencies(),
        'Training Modules': check_modules(),
        'Telegram Handlers': check_telegram_handlers(),
        'FastAPI Application': check_fastapi(),
    }
    
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    for check_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name:.<40} {status}")
    
    all_passed = all(results.values())
    
    print()
    if all_passed:
        print("╔" + "=" * 58 + "╗")
        print("║" + " " * 10 + "✅ SETUP IS VALID - READY TO RUN!" + " " * 17 + "║")
        print("╚" + "=" * 58 + "╝")
        print()
        print("Next steps:")
        print("1. Run: start_core_api.bat (Windows) or follow TELEGRAM_BOT_GUIDE.md")
        print("2. Open Telegram and send /start to your bot")
        print("3. Begin training with /master_path, /arena, etc.")
        return 0
    else:
        print("╔" + "=" * 58 + "╗")
        print("║" + " " * 12 + "❌ SETUP HAS ISSUES" + " " * 25 + "║")
        print("╚" + "=" * 58 + "╝")
        print()
        print("Please fix the issues above and run this script again.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
