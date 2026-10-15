export type CalendarView = "month" | "week";

export function addDays(date: Date, days: number): Date {
    const result = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    result.setDate(result.getDate() + days);
    return result;
}

export function startOfWeek(date: Date): Date {
    const day = date.getDay();
    let diff = day - 1;
    if (day === 0) {
        diff = 6}
    return addDays(date, -diff);
}

export function sameDay(a: Date, b: Date): boolean {
    return a.getFullYear() === b.getFullYear()
        && a.getMonth() === b.getMonth()
        && a.getDate() === b.getDate();
}

export function dateKey(date: Date): string {
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${date.getFullYear()}-${month}-${day}`;
}

export function visibleDays(view: CalendarView, cursor: Date): Date[] {
    let start: Date;
    let count: number;
    if (view === "month") {
        start = startOfWeek(new Date(cursor.getFullYear(), cursor.getMonth(), 1));
        count = 42;
    } else {
        start = startOfWeek(cursor);
        count = 7;}
    const days: Date[] = [];
    for (let i = 0; i < count; i++) {
        days.push(addDays(start, i));
    }
    return days;
}

export function rangeFor(days: Date[]): {from: string; to: string} {
    const first = days[0];
    const afterLast = addDays(days[days.length - 1], 1);
    const to = new Date(afterLast.getTime() - 1);
    return {from: first.toISOString(), to: to.toISOString()};
}

export function moveCursor(view: CalendarView, cursor: Date, direction: number): Date {
    if (view === "month") {
        return new Date(cursor.getFullYear(), cursor.getMonth() + direction, 1);
    }
    return addDays(cursor, direction * 7);
}
