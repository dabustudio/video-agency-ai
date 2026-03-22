# Moon Studio — הוראות עבודה

> לClaude Code — קרא לפני כל שינוי | עודכן מרץ 2026

---

## 1. סדר קריאה חובה — לפני כל פעולה

```
1. docs/ARCHITECTURE.md
2. docs/WORKING_INSTRUCTIONS.md  ← אתה כאן
3. memory/business_context.json
4. agents/orchestrator.md
5. brain/router.md
```

רק אחרי שקראת את כולם — תתחיל לעבוד.

---

## 2. עשה תמיד

- קרא את `CLAUDE.md` ו-`business_context.json` לפני כל פעולה
- קרא מ-Supabase (tools/supabase.md) לפני כל עדכון סטטוס — לא לסמוך על זיכרון session
- שמור כל תוצר ב-`output/` בתיקייה הנכונה
- עשה commit לאחר כל שינוי עם tag: `[agent:שם]`, `[brain]`, `[memory]`, `[tools]`
- Tone: חברי אבל אסרטיבי — בכל תקשורת עם לקוחות

## 2. אל תעשה לעולם

- ❌ אל תדרוס `memory/business_context.json` — רק דביר מעדכן
- ❌ אל תשלח מייל / הצעת מחיר / חשבונית ללקוח — מייצרים, דביר שולח
- ❌ אל תאשר הנחה מעל 15% לבד — תמיד Escalate
- ❌ אל תמחק מ-`output/` — רק לארכב
- ❌ אל תשנה `agents/` ו-`brain/` בלי לתעד ב-commit
- ❌ אל תכתוב תוכן שיווקי בשם הסטודיו עד שדביר יספק דוגמאות סגנון

---

## 3. איך להוסיף סוכן חדש — צ'קליסט

1. צור `agents/[שם].md` עם המבנה הסטנדרטי (ראה סעיף 4)
2. הוסף את הסוכן לטבלת הסוכנים ב-`agents/orchestrator.md`
3. הוסף routing rule ב-`brain/router.md` — מתי לנתב אליו
4. הוסף תיקייה ב-`output/` אם יש תוצרים חדשים
5. עדכן `CLAUDE.md` אם יש כלל חדש שחל על כולם
6. `commit: [agent:new] add [שם] agent`
7. תעד ב-`agents/README.md`

---

## 4. מבנה סטנדרטי לקובץ סוכן

```markdown
# [שם] Agent — Moon Studio

## זהות
[מי הסוכן, מה הוא עושה, מה הוא לא עושה]

## קרא תמיד קודם
memory/business_context.json

## אחריות
[רשימת המשימות]

## Output Schema
[פורמט תוצר מוגדר]

## Eval Criteria
[3-5 שאלות בדיקה לפני כל תוצר]

## Escalate תמיד
[מתי לעצור ולשאול את דביר]
```

---

## 5. איך לעדכן מחירים / שירותים

> ⚠️ שינוי מחירים משפיע על **כל** הסוכנים שמשתמשים ב-`business_context.json`

1. פתח `memory/business_context.json`
2. עדכן תחת `services.production` ו-`pricing_tiers`
3. עדכן את הטבלה ב-`agents/finance.md` בהתאם
4. `commit: [memory] update pricing — [תיאור השינוי]`
5. הודע לדביר שהמחירים עודכנו

---

## 6. איך לעדכן סגמנטי יעד

שינוי ב-`target_segments` משפיע על כל לוגיקת ה-escalation:

1. עדכן `clients.target_segments` ב-`business_context.json`
2. עדכן את רשימת ה-escalation ב-`agents/orchestrator.md`
3. עדכן את ה-routing rule ב-`brain/router.md`
4. עדכן `agents/project_manager.md` — רשימת הסגמנטים לסיווג
5. `commit: [brain] update target segments`

---

## 7. איך לחבר את Supabase

1. פתח `tools/supabase.md`
2. הוסף credentials ל-`.env` (לא לcommit!)
3. אמת שהטבלאות קיימות עם שאילתת הבדיקה בסוף הקובץ
4. `commit: [tools] connect Supabase CRM`

---

## 8. Commit Conventions — חובה

| תג | מתי להשתמש |
|----|------------|
| `[agent:orchestrator]` | שינוי בlogic של ה-orchestrator |
| `[agent:pm]` | שינוי ב-project_manager.md |
| `[agent:finance]` | שינוי ב-finance.md |
| `[agent:client-relations]` | שינוי ב-client_relations.md |
| `[agent:marketing]` | שינוי ב-marketing.md |
| `[agent:content]` | שינוי ב-content.md |
| `[agent:production]` | שינוי ב-production_coord.md |
| `[agent:new]` | הוספת סוכן חדש |
| `[brain]` | שינוי ב-router.md |
| `[memory]` | עדכון business_context.json |
| `[tools]` | הוספת/עדכון חיבור לכלי חיצוני |
| `[docs]` | עדכון מסמכי docs/ |
| `[output]` | שינוי במבנה תיקיית output/ |
| `[fix]` | תיקון בעיה בלוגיקה קיימת |

---

## 9. Context Management — כשהשיחה ארוכה

**Context Trimming (לשיחות שוטפות):**
- שמור רק 10 הפניות האחרונות + summary מתחילת המשימה
- מחק ניסיונות כושלים, שגיאות שכבר תוקנו, מידע ביניים לא-רלוונטי

**Context Compression (לפרויקטים ארוכים):**
- צור summary paragraph — מה הושג, מה הוחלט, מה הצעד הבא
- שמור ב-`output/projects/[שם]/session_summary.md`

---

## 10. Troubleshooting

**הסוכן מייצר תוצאה לא נכונה:**
1. בדוק אם קרא את `business_context.json` לאחרונה
2. בדוק אם ה-`eval_criteria` רצו ועברו
3. בדוק commit history — האם הקובץ שונה לאחרונה

**הסוכן עושה escalate על הכל:**
1. בדוק את רשימת ה-Escalate בקובץ הסוכן — אולי הסף נמוך מדי
2. עדכן את הסף — לדביר לאשר שינויים ב-escalation rules

**שאילתת Supabase נכשלת:**
1. בדוק שה-`.env` טעון: `source .env`
2. בדוק שה-URL והמפתח נכונים ב-supabase.com → Settings → API
3. אמת שמות טבלאות מול הסכמה האמיתית

---

## 11. מה לא לגעת בו בלי לשאול את דביר

- ❌ `memory/business_context.json` — מחירים, לקוחות, העדפות
- ❌ רשימת סגמנטי היעד ב-`router.md`
- ❌ כללי escalation — הסף להעלות לדביר
- ❌ תנאי תשלום ומדיניות הנחות
- ❌ Tone & Voice — איך מדברים עם לקוחות
- ❌ שליחת כל מייל / הצעה / חשבונית החוצה
- ❌ כתיבה שיווקית בשם הסטודיו לפני שיש דוגמאות סגנון
