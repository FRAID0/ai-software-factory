import sys
from model_gateway.gateway import ModelGateway
from shared.schemas.models import ProviderType
from shared.utilities.config import get_config
from shared.utilities.logger import get_logger, setup_logging


def main() -> int:
    setup_logging(level="INFO")
    logger = get_logger("verify_setup")

    print("\n" + "=" * 60)
    print("   AI SOFTWARE FACTORY - SETUP VERIFICATION")
    print("=" * 60)

    # 1. Check Python version
    py_version = sys.version_info
    print(f"\n[1] Python Runtime: {py_version.major}.{py_version.minor}.{py_version.micro}")
    if py_version < (3, 12):
        logger.warning("Recommended Python version is 3.12 or newer.")
    else:
        print("    -> Python version requirement (>=3.12) satisfied.")

    # 2. Check Configuration & Environment Keys
    config = get_config()
    print(f"\n[2] Environment Configuration (FACTORY_ENV={config.factory_env}):")
    providers_status = {
        "Gemini": bool(config.gemini_api_key),
        "Groq": bool(config.groq_api_key),
        "OpenRouter": bool(config.openrouter_api_key),
    }

    configured_count = 0
    for name, is_set in providers_status.items():
        status_str = "CONFIGURED" if is_set else "NOT CONFIGURED (check .env)"
        print(f"    - {name:<12}: {status_str}")
        if is_set:
            configured_count += 1

    # 3. Model Gateway Initialization
    print("\n[3] Model Gateway Initialization:")
    gateway = ModelGateway(config=config)
    available = gateway.get_available_providers()
    print(f"    - Registered adapters   : {len(gateway._providers)}")
    print(f"    - Active providers      : {[p.value for p in available]}")

    if configured_count == 0:
        print("\n[!] Notice: No external provider API keys detected.")
        print("    You can still run automated tests using MockProvider.")
    else:
        print(f"\n[+] Ready! {configured_count} provider(s) active.")

    print("\n" + "=" * 60)
    print("Verification completed successfully.")
    print("=" * 60 + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

