"""Constants for the Electricity Tarif integration."""
from homeassistant.const import Platform

DOMAIN = "tarif_edf"
CONTRACT_TYPE_BASE = "base"
CONTRACT_TYPE_HPHC = "hphc"

# Valeurs par défaut pour les tarifs
DEFAULT_HC_PRICE = 0.1470  # Prix par défaut en heures creuses
DEFAULT_HP_PRICE = 0.1841  # Prix par défaut en heures pleines
DEFAULT_BASE_PRICE = 0.1740  # Prix par défaut pour le tarif base

PLATFORMS = [Platform.SENSOR]
