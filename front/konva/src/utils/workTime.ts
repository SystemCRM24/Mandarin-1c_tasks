import { DateTime, DateTimeUnit, Duration, Interval } from "luxon";
import { TimeRange } from "./time";

/**
 * Типизация интервала для рабочего дня который проиходит ответом от сервера.
 */
export type RawInterval = { start: string; end: string };


export class WorkTime {
  /**
   * Массив временных интервалов, которые соответствуют рабочему времени.
   */
  intervals: Interval[];

  /**
   * Интервал, который соовтетствеует 1 дате начала рабочего периода и последней дате окончания.
   */
  total: Interval;

  /**
   * @param intervals Массив рабочих интервалов.
   */
  constructor(intervals: RawInterval[]) {
    this.intervals = intervals.map((interval) =>
      Interval.fromDateTimes(
        DateTime.fromISO(interval.start), 
        DateTime.fromISO(interval.end)
      )
    );
    this.total = Interval.fromDateTimes(
      this.intervals[0].start!, 
      this.intervals[this.intervals.length - 1].end!
    );
  }

  /**
   * Подсчитывает продолжительность рабочего времени.
   * @param to До какого datetime нужно посчитать.
   * @param from От какого datetime нужно посчитать. Если не указано, берется первая дата из workIntervals.
   * @returns Продолжительность запрашиваемого рабочего времени.
   */
  calcWorkDuration(to: DateTime, from: DateTime | null = null) {
    from = from || this.total.start!;
    const requestInterval = Interval.fromDateTimes(from, to);
    let duration = Duration.fromMillis(0);
    let stopFlag = false;
    for (const interval of this.intervals) {
      const intersection = requestInterval.intersection(interval);
      if (intersection !== null && intersection.isValid ) {
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
  calcNonWorkDuration(to: DateTime, from: DateTime | null = null) {
    from = from || this.total.start!;
    const requestInterval = Interval.fromDateTimes(from, to);
    const workDuration = this.calcWorkDuration(to, from);
    return requestInterval.toDuration().minus(workDuration);
  }

  /**
   * Возвращает нерабочее время округленное с левой стороны до resolution
   * @param to До какого datetime нужно посчитать.
   * @param resolution Значение разрешения, до какой даты нужно округлить
   */
  calcOuterNonWorkDuration(to: DateTime, resolution: DateTimeUnit) {
    const from = this.total.start!.startOf(resolution);
    return this.calcNonWorkDuration(to, from);
  }

  /**
   * Проверяет, находится ли дата в промежутке рабочего времени
   * @param date Дата для проверки
   * @returns true если находится, false в противном случае.
   */
  dateOnWorkTime(date: DateTime) {
    for ( const workInterval of this.intervals ) {
      if ( workInterval.contains(date) ) {
        return true;
      }
    }
    return false;
  }

  onTaskDrag(taskTime: TimeRange, initialTime: TimeRange, newTime: TimeRange): TimeRange {
    let taskStart = DateTime.fromMillis(taskTime.start as number);
    let taskEnd = DateTime.fromMillis(taskTime.end as number);
    const stepAbs = 60000;
    let step = Duration.fromMillis(stepAbs);
    let diff = Duration.fromMillis((newTime.start as number) - (initialTime.start as number));
    if ( diff.milliseconds < 0 ) {
      step = step.negate();
      diff = diff.negate();
    }
    const diffAbs = diff.toMillis();
    const calculate = (diff: number, date: DateTime): DateTime => {
      while ( diff > 0 ) {
        date = date.plus(step);
        if ( this.dateOnWorkTime(date) || !(this.total.contains(date)) ) {
          diff -= stepAbs;
        }
      }
      return date;
    }
    taskStart = calculate(diffAbs, taskStart);
    taskEnd = calculate(diffAbs, taskEnd);
    return {start: taskStart.toMillis(), end: taskEnd.toMillis()};
  }

  onTaskResize(oldTime: TimeRange, newTime: TimeRange,  direction: string): TimeRange {
    let start = DateTime.fromMillis(oldTime.start as number);
    let end = DateTime.fromMillis(oldTime.end as number);
    let oldInterval = Interval.fromDateTimes(start, end).toDuration();
    oldInterval = oldInterval.minus(this.calcNonWorkDuration(end, start));
    let newInterval = Interval.fromDateTimes(
      DateTime.fromMillis(newTime.start as number),
      DateTime.fromMillis(newTime.end as number),
    );

    const stepAbs = 60000;
    let step = Duration.fromMillis(stepAbs);
    let diff = newInterval.toDuration().minus(oldInterval);
    if ( diff.milliseconds < 0 ) {
      step = step.negate();
      diff = diff.negate();
    }
    let diffAbs = diff.toMillis();

    switch ( direction ) {
      case 'lx':
        while ( diffAbs > 0 ) {
          start = start.minus(step);
          // diffAbs -= stepAbs;
          if ( this.dateOnWorkTime(start) || !(this.total.contains(start)) ) {
            diffAbs -= stepAbs;
          }
        }
        break;
      case 'rx':
      default:
        while ( diffAbs > 0 ) {
          end = end.plus(step);
          // diffAbs -= stepAbs;
          if ( this.dateOnWorkTime(end) || !(this.total.contains(end)) ) {
            diffAbs -= stepAbs;
          }
        }
    }
    return {start: start.toMillis(), end: end.toMillis()};
  }
}
