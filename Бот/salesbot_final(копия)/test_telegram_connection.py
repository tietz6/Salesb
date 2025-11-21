#!/usr/bin/env python3
"""
Test script to verify Telegram bot token and connectivity
"""
import os
import asyncio
import sys

# Set token from environment or use the one from the config
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN") or "8029409301:AAGpKsSxQ_rdQJm_5kR6hk_E5JgOoQLNAgI"

async def test_connection():
    """Test connection to Telegram API"""
    try:
        from aiogram import Bot
        
        print("=" * 60)
        print("Testing Telegram Bot Connection")
        print("=" * 60)
        print(f"\n✅ Token configured: {TELEGRAM_TOKEN[:20]}...{TELEGRAM_TOKEN[-10:]}")
        print(f"✅ Aiogram library imported successfully")
        
        # Create bot instance
        bot = Bot(token=TELEGRAM_TOKEN)
        print(f"✅ Bot instance created")
        
        # Try to get bot info
        print(f"\n⏳ Attempting to connect to Telegram API...")
        try:
            me = await bot.get_me()
            print(f"\n🎉 SUCCESS! Bot is connected!")
            print(f"=" * 60)
            print(f"Bot Info:")
            print(f"  ID: {me.id}")
            print(f"  Name: {me.first_name}")
            print(f"  Username: @{me.username}")
            print(f"  Can Join Groups: {me.can_join_groups}")
            print(f"  Can Read All Group Messages: {me.can_read_all_group_messages}")
            print(f"=" * 60)
            
            # Clear any webhooks to ensure polling works
            print(f"\n⏳ Removing any existing webhooks...")
            await bot.delete_webhook(drop_pending_updates=True)
            webhook_info = await bot.get_webhook_info()
            if webhook_info.url:
                print(f"⚠️  Warning: Webhook still set to {webhook_info.url}")
            else:
                print(f"✅ No webhook set - polling mode ready")
            
            await bot.session.close()
            return True
            
        except Exception as e:
            print(f"\n❌ FAILED to connect to Telegram API")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            
            if "No address associated with hostname" in str(e) or "gaierror" in str(e):
                print("\n🔍 Diagnosis: Network connectivity issue")
                print("   - The bot cannot reach api.telegram.org")
                print("   - This may be due to:")
                print("     1. No internet connection")
                print("     2. DNS resolution issues")
                print("     3. Firewall/proxy blocking Telegram")
                print("     4. Running in restricted environment")
                print("\n💡 Solutions:")
                print("   1. Check internet connectivity")
                print("   2. Try using a proxy (if available)")
                print("   3. Check firewall settings")
            elif "Unauthorized" in str(e) or "401" in str(e):
                print("\n🔍 Diagnosis: Invalid bot token")
                print("   - The token is incorrect or has been revoked")
                print("\n💡 Solutions:")
                print("   1. Get a new token from @BotFather in Telegram")
                print("   2. Update the token in start_core_api.bat")
            else:
                print("\n🔍 Diagnosis: Unknown error")
                print("   - Check the error message above for details")
            
            await bot.session.close()
            return False
            
    except ImportError as e:
        print(f"❌ Failed to import aiogram: {e}")
        print("💡 Solution: Install aiogram with: pip install aiogram>=3.0.0")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main entry point"""
    result = asyncio.run(test_connection())
    
    if result:
        print("\n✅ Your Telegram bot is ready to use!")
        print("   Run: python telegram_bot.py")
        print("   Or: start_core_api.bat")
        return 0
    else:
        print("\n❌ Bot connection failed - see diagnosis above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
