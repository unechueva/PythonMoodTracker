from datetime import timedelta
from django.utils import timezone
from .models import Entry

def get_entries_for_period(user, days: int):
    today = timezone.now().date()
    start_date = today - timedelta(days=days)
    return Entry.objects.filter(
        user=user,
        date__gte=start_date
    ).order_by('-date')

def calculate_average(entries):
    if not entries.exists():
        return 0.0
    total = sum(entry.mood for entry in entries)
    return round(total / entries.count(), 2)

def find_min_max_days(entries):
    if not entries.exists():
        return None, None
    min_entry = entries.order_by('mood').first()
    max_entry = entries.order_by('-mood').first()
    min_days = [e.date for e in entries if e.mood == min_entry.mood]
    max_days = [e.date for e in entries if e.mood == max_entry.mood]
    return min_days, max_days

def calculate_streaks(entries):
    if not entries.exists():
        return 0, 0
    sorted_entries = list(entries.order_by('date'))
    good_streak = 0
    bad_streak = 0
    current_good = 0
    current_bad = 0
    for entry in sorted_entries:
        if entry.mood >= 4:
            current_good += 1
            current_bad = 0
        elif entry.mood <= 2:
            current_bad += 1
            current_good = 0
        else:
            current_good = 0
            current_bad = 0
        good_streak = max(good_streak, current_good)
        bad_streak = max(bad_streak, current_bad)
    return good_streak, bad_streak

def build_report(entries):
    avg_mood = calculate_average(entries)
    min_days, max_days = find_min_max_days(entries)
    good_streak, bad_streak = calculate_streaks(entries)
    if avg_mood <= 2:
        recommendation = "Похоже, период был тяжёлым. Попробуй немного снизить нагрузку."
    elif avg_mood <= 4:
        recommendation = "Период в целом стабильный. Продолжай в том же духе!"
    else:
        recommendation = "Неделя была наполнена позитивом — отлично!"
    return {
        'average_mood': avg_mood,
        'entry_count': entries.count(),
        'min_days': min_days or [],
        'max_days': max_days or [],
        'good_streak': good_streak,
        'bad_streak': bad_streak,
        'recommendation': recommendation,
    }
