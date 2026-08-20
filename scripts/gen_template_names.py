"""Generate panel/template-names.js from seed_templates.json."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = ROOT / "custom_components/fridge_assistant/data/seed_templates.json"
OUT_PATH = ROOT / "custom_components/fridge_assistant/panel/template-names.js"

# fr/en display names for builtin seed templates (nl name is the seed default).
NAMES: dict[str, tuple[str, str]] = {
    "krop-sla": ("Laitue en pomme", "Head lettuce"),
    "spinazie": ("Épinards", "Spinach"),
    "wortel": ("Carotte", "Carrot"),
    "broccoli": ("Brocoli", "Broccoli"),
    "komkommer": ("Concombre", "Cucumber"),
    "paprika": ("Poivron", "Bell pepper"),
    "ui": ("Oignon", "Onion"),
    "aardappel": ("Pomme de terre", "Potato"),
    "tomaat": ("Tomate", "Tomato"),
    "bloemkool": ("Chou-fleur", "Cauliflower"),
    "courgette": ("Courgette", "Zucchini"),
    "champignons": ("Champignons", "Mushrooms"),
    "sperziebonen": ("Haricots verts", "Green beans"),
    "prei": ("Poireau", "Leek"),
    "andijvie": ("Scarole", "Endive"),
    "boerenkool": ("Chou frisé", "Kale"),
    "banaan": ("Banane", "Banana"),
    "appel": ("Pomme", "Apple"),
    "aardbeien": ("Fraises", "Strawberries"),
    "druiven": ("Raisins", "Grapes"),
    "citroen": ("Citron", "Lemon"),
    "sinaasappel": ("Orange", "Orange"),
    "peer": ("Poire", "Pear"),
    "blauwe-bessen": ("Myrtilles", "Blueberries"),
    "mango": ("Mangue", "Mango"),
    "avocado": ("Avocat", "Avocado"),
    "kiwi": ("Kiwi", "Kiwi"),
    "melk": ("Lait", "Milk"),
    "yoghurt": ("Yaourt", "Yogurt"),
    "jonge-kaas": ("Fromage jeune", "Young cheese"),
    "oude-kaas": ("Fromage affiné", "Aged cheese"),
    "roomkaas": ("Fromage à tartiner", "Cream cheese"),
    "boter": ("Beurre", "Butter"),
    "slagroom": ("Crème fouettée", "Whipping cream"),
    "kwark": ("Fromage blanc", "Quark"),
    "karnemelk": ("Babeurre", "Buttermilk"),
    "creme-fraiche": ("Crème fraîche", "Crème fraîche"),
    "geraspte-kaas": ("Fromage râpé", "Grated cheese"),
    "kipfilet-rauw": ("Blanc de poulet cru", "Raw chicken breast"),
    "gehakt-rauw": ("Viande hachée crue", "Raw ground meat"),
    "spek": ("Bacon", "Bacon"),
    "kip-gebraden": ("Poulet rôti", "Roast chicken"),
    "rookworst": ("Saucisse fumée", "Smoked sausage"),
    "ham-vleeswaren": ("Jambon", "Ham"),
    "salami": ("Salami", "Salami"),
    "biefstuk-rauw": ("Steak cru", "Raw steak"),
    "hamburger-rauw": ("Steak haché cru", "Raw burger patty"),
    "zalm-rauw": ("Saumon cru", "Raw salmon"),
    "garnalen": ("Crevettes", "Shrimp"),
    "witvis-kabeljauw": ("Poisson blanc", "White fish"),
    "gerookte-zalm": ("Saumon fumé", "Smoked salmon"),
    "tonijn-blik-open": ("Thon en conserve (ouvert)", "Canned tuna (open)"),
    "haring": ("Hareng", "Herring"),
    "macaroni-met-vlees": ("Macaroni à la viande", "Macaroni with meat"),
    "nasi": ("Nasi", "Nasi goreng"),
    "verse-soep": ("Soupe fraîche", "Fresh soup"),
    "stamppot": ("Purée-hachis", "Stamppot"),
    "rijst-gekookt": ("Riz cuit", "Cooked rice"),
    "pasta-gekookt": ("Pâtes cuites", "Cooked pasta"),
    "curry": ("Curry", "Curry"),
    "lasagne": ("Lasagnes", "Lasagna"),
    "pannenkoeken": ("Crêpes", "Pancakes"),
    "bami": ("Bami", "Bami goreng"),
    "aardappelpuree": ("Purée de pommes de terre", "Mashed potatoes"),
    "groentesoep": ("Soupe aux légumes", "Vegetable soup"),
    "brood": ("Pain", "Bread"),
    "croissant": ("Croissant", "Croissant"),
    "wraps": ("Wraps", "Wraps"),
    "bagels": ("Bagels", "Bagels"),
    "beschuit": ("Biscottes", "Rusks"),
    "krentenbollen": ("Petits pains aux raisins", "Currant buns"),
    "pesto": ("Pesto (ouvert)", "Pesto (open)"),
    "mayonaise-open": ("Mayonnaise (ouverte)", "Mayonnaise (open)"),
    "ketchup-open": ("Ketchup (ouverte)", "Ketchup (open)"),
    "hummus": ("Houmous", "Hummus"),
    "tomatensaus-open": ("Sauce tomate (ouverte)", "Tomato sauce (open)"),
    "mosterd-open": ("Moutarde (ouverte)", "Mustard (open)"),
    "sojasaus-open": ("Sauce soja (ouverte)", "Soy sauce (open)"),
    "appelmoes-open": ("Compote de pommes (ouverte)", "Apple sauce (open)"),
    "verse-pesto-koelvers": ("Pesto frais (réfrigéré)", "Fresh pesto (chilled)"),
    "verse-jus": ("Jus d'orange frais", "Fresh orange juice"),
    "open-witte-wijn": ("Vin blanc ouvert", "Open white wine"),
    "open-rode-wijn": ("Vin rouge ouvert", "Open red wine"),
    "plantaardige-melk-open": ("Lait végétal (ouvert)", "Plant milk (open)"),
    "vruchtensap-open": ("Jus de fruits (ouvert)", "Fruit juice (open)"),
    "eieren": ("Œufs", "Eggs"),
    "gekookt-ei": ("Œuf dur", "Boiled egg"),
    "restjes-algemeen": ("Restes", "Leftovers"),
    "restjes-ovenschotel": ("Restes de gratin", "Leftover casserole"),
    "tofu-open": ("Tofu (ouverte)", "Tofu (open)"),
    "olijven-open": ("Olives (ouvertes)", "Olives (open)"),
    "verse-basilicum": ("Basilic frais", "Fresh basil"),
    "tuinbonen": ("Fèves", "Broad beans"),
    "doperwten": ("Petits pois", "Peas"),
    "mais": ("Maïs", "Corn"),
    "frambozen": ("Framboises", "Raspberries"),
    "meloen": ("Melon", "Melon"),
    "pizza-margherita": ("Pizza margherita", "Margherita pizza"),
    "pindakaas": ("Beurre de cacahuète", "Peanut butter"),
}


def main() -> None:
    with SEED_PATH.open(encoding="utf-8") as f:
        seed = json.load(f)
    ids = [t["id"] for t in seed["templates"]]
    missing = [i for i in ids if i not in NAMES]
    extra = [i for i in NAMES if i not in ids]
    if missing:
        raise SystemExit(f"Missing translations for: {missing}")
    if extra:
        raise SystemExit(f"Unknown template ids in NAMES: {extra}")

    lines = [
        "// Builtin seed template display names (nl names live in seed_templates.json).",
        "// i18n: fr and en only; nl falls back to the seed name.",
        "",
        "export const TEMPLATE_NAMES = {",
    ]
    for tid in ids:
        fr, en = NAMES[tid]
        lines.append(
            f'  "{tid}": {{ fr: {json.dumps(fr, ensure_ascii=False)}, '
            f"en: {json.dumps(en, ensure_ascii=False)} }},"
        )
    lines += [
        "};",
        "",
        "/** Localized display name for a template row (custom/user overrides keep stored name). */",
        "export function templateDisplayName(tpl, lang) {",
        '  if (!tpl) return "";',
        '  if (tpl.custom) return tpl.name || "";',
        "  const row = TEMPLATE_NAMES[tpl.id];",
        "  if (row && row[lang]) return row[lang];",
        '  return tpl.name || "";',
        "}",
        "",
    ]
    OUT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"Wrote {OUT_PATH} ({len(ids)} templates)")


if __name__ == "__main__":
    main()
