import { DateTime, DateTimeUnit, Duration, Interval } from "luxon";
import { TimeRange } from "./time";
/**
 * Типизация интервала для рабочего дня который проиходит ответом от сервера.
 */
export type RawInterval = {
    start: string;
    end: string;
};
export declare class WorkTime {
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
    constructor(intervals: RawInterval[]);
    /**
     * Подсчитывает продолжительность рабочего времени.
     * @param to До какого datetime нужно посчитать.
     * @param from От какого datetime нужно посчитать. Если не указано, берется первая дата из workIntervals.
     * @returns Продолжительность запрашиваемого рабочего времени.
     */
    calcWorkDuration(to: DateTime, from?: DateTime | null): Duration<true>;
    /**
     * Подсчитывает продолжительность нерабочего времени.
     * @param to До какого datetime нужно посчитать.
     * @param from От какого datetime нужно посчитать. Если не указано, берется первая дата из workIntervals.
     * @returns Продолжительность запрашиваемого нерабочего времени.
     */
    calcNonWorkDuration(to: DateTime, from?: DateTime | null): Duration<true> | Duration<false>;
    /**
     * Возвращает нерабочее время округленное с левой стороны до resolution
     * @param to До какого datetime нужно посчитать.
     * @param resolution Значение разрешения, до какой даты нужно округлить
     */
    calcOuterNonWorkDuration(to: DateTime, resolution: DateTimeUnit): Duration<true> | Duration<false>;
    /**
     * Проверяет, находится ли дата в промежутке рабочего времени
     * @param date Дата для проверки
     * @returns true если находится, false в противном случае.
     */
    dateOnWorkTime(date: DateTime): boolean;
    onTaskDrag(taskTime: TimeRange, initialTime: TimeRange, newTime: TimeRange): TimeRange;
    onTaskResize(oldTime: TimeRange, newTime: TimeRange, direction: string): TimeRange;
}
