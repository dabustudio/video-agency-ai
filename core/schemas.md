# Core Schemas — Moon Studio

> הגדרות JSON מרכזיות שכל הסוכנים משתמשים בהן. אל תשנה ללא commit מתועד.

---

## 1. Lead Schema (ליד)

**מנוהל על ידי:** Project Manager Agent
**נשמר ב:** `output/projects/leads.json`

```json
{
  "lead_id": "YYYY-MM-DD-שם",
  "name": "",
  "phone": "",
  "email": "",
  "source": "פה לאוזן | הפניה | LinkedIn | Instagram | אחר",
  "segment": "פרטי | עסק קטן | היי-טק | מסעדה | מותג | משרד פרסום",
  "service_requested": "",
  "budget_indicated": null,
  "date_entered": "YYYY-MM-DD",
  "status": "ליד | בטיפול | הצעה נשלחה | סגור-כן | סגור-לא",
  "priority": "גבוהה | רגילה",
  "quote_id": null,
  "project_id": null,
  "notes": ""
}
```

**כלל אוטומטי:** אם `segment` הוא `היי-טק | מסעדה | מותג | משרד פרסום` → `priority: "גבוהה"` + התראה מיידית לדביר.

---

## 2. Project Schema (פרויקט פעיל)

**מנוהל על ידי:** Project Manager Agent
**נשמר ב:** `output/projects/[project_id]/project.json`

```json
{
  "project_id": "YYYY-MM-DD-שם-לקוח",
  "lead_id": "",
  "client_name": "",
  "client_contact": {
    "phone": "",
    "email": ""
  },
  "service_type": "יום צילום מלא | חצי יום | סשן סושיאל | עריכה | מושן | קורס | אחר",
  "description": "",
  "status": "בריף | צילום | עריכה | אישור לקוח | סגור",
  "dates": {
    "opened": "YYYY-MM-DD",
    "shoot": null,
    "delivery_target": null,
    "closed": null
  },
  "quote_id": null,
  "invoice_id": null,
  "amount_total": null,
  "amount_paid": null,
  "files": {
    "brief": null,
    "script": null,
    "call_sheet": null,
    "raw_footage": null,
    "final_delivery": null
  },
  "notes": ""
}
```

**Escalation trigger:** אם `status` לא התקדם ב-48 שעות → התראה לדביר.

---

## 3. Quote Schema (הצעת מחיר)

**מנוהל על ידי:** Finance Agent
**נשמר ב:** `output/quotes/[quote_id]/`

```json
{
  "quote_id": "Q-YYYY-MM-DD-שם",
  "project_id": "",
  "client_name": "",
  "date_created": "YYYY-MM-DD",
  "valid_until": "YYYY-MM-DD",
  "line_items": [
    {
      "service": "",
      "quantity": 1,
      "unit_price": 0,
      "total": 0
    }
  ],
  "subtotal": 0,
  "vat_rate": 0.18,
  "vat_amount": 0,
  "total_with_vat": 0,
  "discount_percent": 0,
  "discount_approved_by": null,
  "payment_terms": "50% מקדמה | 50% במסירה",
  "status": "טיוטה | ממתין לאישור דביר | נשלח | אושר | נדחה",
  "pdf_path": null,
  "notes": ""
}
```

**Escalation triggers:**
- `total_with_vat > 15000` → `status: "ממתין לאישור דביר"` לפני שליחה
- `discount_percent > 10` → עצור, שאל את דביר, מלא `discount_approved_by`

---

## 4. Invoice Schema (חשבונית)

**מנוהל על ידי:** Finance Agent
**נשמר ב:** `output/invoices/[invoice_id]/`

```json
{
  "invoice_id": "INV-YYYY-MM-DD-שם",
  "quote_id": "",
  "project_id": "",
  "client_name": "",
  "date_issued": "YYYY-MM-DD",
  "due_date": "YYYY-MM-DD",
  "amount_total": 0,
  "amount_paid": 0,
  "payment_date": null,
  "status": "נשלחה | שולמה חלקית | שולמה | פגת תוקף | חוב",
  "pdf_path": null,
  "notes": ""
}
```

**Escalation triggers:**
- `status: "חוב"` + יותר מ-7 ימים → Finance + התראה מיידית לדביר
- `amount_total - amount_paid > 3000` → דוח שבועי חובה

---

## 5. Shoot Schema (יום צילום)

**מנוהל על ידי:** Production Coordinator Agent
**נשמר ב:** `output/production/schedule_YYYY-WXX.json`

```json
{
  "shoot_id": "YYYY-MM-DD-שם-לקוח",
  "project_id": "",
  "client": "",
  "type": "יום מלא | חצי יום | סשן סושיאל",
  "date": "YYYY-MM-DD",
  "call_time": "HH:MM",
  "location": {
    "address": "",
    "maps_link": "",
    "parking": "",
    "notes": ""
  },
  "crew": ["דביר"],
  "equipment": [],
  "special_equipment_needed": false,
  "special_equipment_order_id": null,
  "checklist": {
    "call_sheet_sent": false,
    "location_confirmed": false,
    "equipment_checked": false,
    "advance_payment_confirmed": false,
    "raw_backup_done": false
  },
  "status": "מתוכנן | אושר | צולם | גובה"
}
```

---

## 6. Content Schema (תוכן)

**מנוהל על ידי:** Content Agent
**נשמר ב:** `output/content/[project_id]/`

```json
{
  "content_id": "YYYY-MM-DD-שם-פרויקט",
  "project_id": "",
  "type": "script | brief | captions | studio-content | cold-outreach",
  "client": "",
  "platform": "instagram | youtube | linkedin | whatsapp | other",
  "duration_seconds": null,
  "status": "טיוטה | בעריכה | מאושר | בשימוש",
  "file_path": "",
  "dvir_approved": false,
  "notes": ""
}
```

---

## 7. Outreach Schema (פנייה שיווקית)

**מנוהל על ידי:** Marketing Agent
**נשמר ב:** `output/marketing/outreach_log/outreach_log.json`

```json
{
  "outreach_id": "YYYY-MM-DD-שם-חברה",
  "company_name": "",
  "contact_name": "",
  "contact_role": "",
  "platform": "LinkedIn | Email | Instagram | Phone | Other",
  "segment": "היי-טק | מסעדה | מותג | משרד פרסום",
  "message_sent": "",
  "date_sent": "YYYY-MM-DD",
  "response": "אין | חיובי | לא מעוניין | מאוחר יותר",
  "response_date": null,
  "escalated_to_pm": false,
  "notes": ""
}
```

**כלל אוטומטי:** אם `response: "חיובי"` → `escalated_to_pm: true` + העברה מיידית ל-Project Manager.
