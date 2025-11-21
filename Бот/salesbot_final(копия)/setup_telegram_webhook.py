"""
Script to setup Telegram webhook for the bot.
Usage: python setup_telegram_webhook.py <public_url>
Example: python setup_telegram_webhook.py https://your-domain.com
"""

import os
import sys
import requests


def setup_webhook(public_url: str, token: str = None) -> dict:
    """
    Set up Telegram webhook
    
    Args:
        public_url: Your public URL (e.g., https://your-domain.com)
        token: Telegram bot token (if not provided, reads from environment)
    
    Returns:
        dict: Response from Telegram API
    """
    if not token:
        token = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
    
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
    
    # Remove trailing slash from URL
    public_url = public_url.rstrip('/')
    
    # Webhook endpoint
    webhook_url = f"{public_url}/api/telegram/webhook"
    
    # Telegram API URL
    api_url = f"https://api.telegram.org/bot{token}/setWebhook"
    
    print(f"Setting up webhook...")
    print(f"Bot Token: {token[:10]}...{token[-5:]}")
    print(f"Webhook URL: {webhook_url}")
    
    # Set webhook
    response = requests.post(
        api_url,
        json={"url": webhook_url},
        timeout=30
    )
    
    result = response.json()
    
    if result.get("ok"):
        print("\n✅ Webhook set successfully!")
        print(f"Description: {result.get('description', 'N/A')}")
    else:
        print("\n❌ Failed to set webhook!")
        print(f"Error: {result.get('description', 'Unknown error')}")
    
    return result


def get_webhook_info(token: str = None) -> dict:
    """Get current webhook information"""
    if not token:
        token = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
    
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
    
    api_url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
    
    response = requests.get(api_url, timeout=30)
    result = response.json()
    
    if result.get("ok"):
        info = result.get("result", {})
        print("\n📊 Current webhook info:")
        print(f"  URL: {info.get('url', 'Not set')}")
        print(f"  Has custom certificate: {info.get('has_custom_certificate', False)}")
        print(f"  Pending update count: {info.get('pending_update_count', 0)}")
        print(f"  Max connections: {info.get('max_connections', 40)}")
        
        if info.get('last_error_date'):
            print(f"  Last error: {info.get('last_error_message', 'N/A')}")
    
    return result


def delete_webhook(token: str = None) -> dict:
    """Delete the webhook (switch back to polling mode)"""
    if not token:
        token = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
    
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
    
    api_url = f"https://api.telegram.org/bot{token}/deleteWebhook"
    
    print("Deleting webhook...")
    response = requests.post(api_url, timeout=30)
    result = response.json()
    
    if result.get("ok"):
        print("\n✅ Webhook deleted successfully!")
    else:
        print("\n❌ Failed to delete webhook!")
        print(f"Error: {result.get('description', 'Unknown error')}")
    
    return result


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python setup_telegram_webhook.py <public_url>  - Set webhook")
        print("  python setup_telegram_webhook.py info          - Get webhook info")
        print("  python setup_telegram_webhook.py delete        - Delete webhook")
        print("\nExample:")
        print("  python setup_telegram_webhook.py https://your-domain.com")
        print("  python setup_telegram_webhook.py https://abc123.ngrok.io")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    try:
        if command == "info":
            get_webhook_info()
        elif command == "delete":
            delete_webhook()
        else:
            # Assume it's a URL
            public_url = sys.argv[1]
            if not public_url.startswith("http"):
                print("❌ URL must start with http:// or https://")
                sys.exit(1)
            
            setup_webhook(public_url)
            print("\n" + "="*60)
            get_webhook_info()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
