"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.WorkTime = void 0;
const luxon_1 = require("luxon");
class WorkTime {
    /**
     * @param intervals Массив рабочих интервалов.
     */
    constructor(intervals) {
        this.intervals = intervals.map((interval) => luxon_1.Interval.fromDateTimes(luxon_1.DateTime.fromISO(interval.start), luxon_1.DateTime.fromISO(interval.end)));
        this.total = luxon_1.Interval.fromDateTimes(this.intervals[0].start, this.intervals[this.intervals.length - 1].end);
    }
    /**
     * Подсчитывает продолжительность рабочего времени.
     * @param to До какого datetime нужно посчитать.
     * @param from От какого datetime нужно посчитать. Если не указано, берется первая дата из workIntervals.
     * @returns Продолжительность запрашиваемого рабочего времени.
     */
    calcWorkDuration(to, from = null) {
        from = from || this.total.start;
        const requestInterval = luxon_1.Interval.fromDateTimes(from, to);
        let duration = luxon_1.Duration.fromMillis(0);
        let stopFlag = false;
        for (const interval of this.intervals) {
            const intersection = requestInterval.intersection(interval);
            if (intersection !== null && intersection.isValid) {
                duration = duration.plus(intersection.toDuration());
                stopFlag = true;
                continue;
            }
            if (stopFlag) {
                break;
            }
        }
        return duration;
    }
    /**
     * Подсчитывает продолжительность нерабочего времени.
     * @param to До какого datetime нужно посчитать.
     * @param from От какого datetime нужно посчитать. Если не указано, берется первая дата из workIntervals.
     * @returns Продолжительность запрашиваемого нерабочего времени.
     */
    calcNonWorkDuration(to, from = null) {
        from = from || this.total.start;
        const requestInterval = luxon_1.Interval.fromDateTimes(from, to);
        const workDuration = this.calcWorkDuration(to, from);
        return requestInterval.toDuration().minus(workDuration);
    }
    /**
     * Возвращает нерабочее время округленное с левой стороны до resolution
     * @param to До какого datetime нужно посчитать.
     * @param resolution Значение разрешения, до какой даты нужно округлить
     */
    calcOuterNonWorkDuration(to, resolution) {
        const from = this.total.start.startOf(resolution);
        return this.calcNonWorkDuration(to, from);
    }
    /**
     * Проверяет, находится ли дата в промежутке рабочего времени
     * @param date Дата для проверки
     * @returns true если находится, false в противном случае.
     */
    dateOnWorkTime(date) {
        for (const workInterval of this.intervals) {
            if (workInterval.contains(date)) {
                return true;
            }
        }
        return false;
    }
    onTaskDrag(taskTime, initialTime, newTime) {
        let taskStart = luxon_1.DateTime.fromMillis(taskTime.start);
        let taskEnd = luxon_1.DateTime.fromMillis(taskTime.end);
        const stepAbs = 60000;
        let step = luxon_1.Duration.fromMillis(stepAbs);
        let diff = luxon_1.Duration.fromMillis(newTime.start - initialTime.start);
        if (diff.milliseconds < 0) {
            step = step.negate();
            diff = diff.negate();
        }
        const diffAbs = diff.toMillis();
        const calculate = (diff, date) => {
            while (diff > 0) {
                date = date.plus(step);
                if (this.dateOnWorkTime(date) || !(this.total.contains(date))) {
                    diff -= stepAbs;
                }
            }
            return date;
        };
        taskStart = calculate(diffAbs, taskStart);
        taskEnd = calculate(diffAbs, taskEnd);
        return { start: taskStart.toMillis(), end: taskEnd.toMillis() };
    }
    onTaskResize(oldTime, newTime, direction) {
        let start = luxon_1.DateTime.fromMillis(oldTime.start);
        let end = luxon_1.DateTime.fromMillis(oldTime.end);
        let oldInterval = luxon_1.Interval.fromDateTimes(start, end).toDuration();
        oldInterval = oldInterval.minus(this.calcNonWorkDuration(end, start));
        let newInterval = luxon_1.Interval.fromDateTimes(luxon_1.DateTime.fromMillis(newTime.start), luxon_1.DateTime.fromMillis(newTime.end));
        const stepAbs = 60000;
        let step = luxon_1.Duration.fromMillis(stepAbs);
        let diff = newInterval.toDuration().minus(oldInterval);
        if (diff.milliseconds < 0) {
            step = step.negate();
            diff = diff.negate();
        }
        let diffAbs = diff.toMillis();
        switch (direction) {
            case 'lx':
                while (diffAbs > 0) {
                    start = start.minus(step);
                    // diffAbs -= stepAbs;
                    if (this.dateOnWorkTime(start) || !(this.total.contains(start))) {
                        diffAbs -= stepAbs;
                    }
                }
                break;
            case 'rx':
            default:
                while (diffAbs > 0) {
                    end = end.plus(step);
                    // diffAbs -= stepAbs;
                    if (this.dateOnWorkTime(end) || !(this.total.contains(end))) {
                        diffAbs -= stepAbs;
                    }
                }
        }
        return { start: start.toMillis(), end: end.toMillis() };
    }
}
exports.WorkTime = WorkTime;
