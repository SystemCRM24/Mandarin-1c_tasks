import { useCallback, useEffect, useMemo, useState } from 'react';

import { useAppContext } from '../Context';
import Header from '../Header';
import { KonvaTimeline } from "../Konva";
import Alerts from '../Alerts';
import { updateBXTask } from '../../api';

import "./Main.css";



function Main() {
    const {
        permission,
        workIntervals,
        step,
        resolution,
        range,
        resources,
        tasks,
        setTasks,
        errors,
        setErrors,
        wsConnection
    } = useAppContext();

    const nearestStamps = useMemo(
        () => {
            return {
                "1min": 1, 
                "5min": 5, 
                "10min": 10, 
                "15min": 15, 
                "30min": 30, 
                "1hrs": 60, 
                "2hrs": 120, 
                "6hrs": 360, 
                "12hrs": 720, 
                "1day": 1440, 
                "1week": 10080, 
                "2weeks": 20160
            }
        },
        []
    );

    const roundTSToNearest = useCallback(
        (ts) => {
            const nearest = nearestStamps[step] * 60000;
            ts += 10800000;
            const result = Math.round(ts / nearest) * nearest;
            return result - 10800000;            
        },
        [step, nearestStamps]
    );

    const alignDuration = useCallback(
        (task, changedTask) => {
            const diff = (task.time.end - task.time.start) !== (changedTask.time.end - changedTask.time.start);
            if ( diff ) {
                if ( changedTask.time.start !== task.time.start ) {
                    const nearesStart = roundTSToNearest(changedTask.time.start);
                    changedTask.time.start = nearesStart;
                }
                if ( changedTask.time.end !== task.time.end ) {
                    const nearestEnd = roundTSToNearest(changedTask.time.end);
                    changedTask.time.end = nearestEnd;
                }
            }
            return changedTask;
        },
        [roundTSToNearest]
    );

    const sendRequest = useCallback(
        (task) => {
            task.deadline = (new Date(task.deadline)).toISOString();
            task.time.start = (new Date(task.time.start)).toISOString();
            task.time.end = (new Date(task.time.end)).toISOString();
            const json_string = JSON.stringify(task);
            wsConnection.send(json_string);
        },
        [wsConnection]
    );

    const [changedTask, setChangedTask] = useState(null);
    useEffect(
        () => {
            if ( changedTask === null ) {
                return;
            }
            const newTasks = tasks.map(
                (task) => {
                    if ( task.id === changedTask.id ) {
                        return alignDuration(task, changedTask);
                    }
                    return task;
                }
            );
            setTasks(newTasks);
            updateBXTask(changedTask);
        },
        [changedTask]
    );

    const onErrors = useCallback(
        (widgetErrors) => {
            if (JSON.stringify(errors) !== JSON.stringify(widgetErrors)) {
                setErrors(widgetErrors);
            }
        },
        [setErrors]
    );

    const onTaskClick = useCallback(
        (task) => {
            const url = `https://office.ra-mandarin.com/company/personal/user/1/tasks/task/view/${task.id}/`;
            window.open(url, '_blank');
        },
        []
    );

    return (
        <>
            <Header/>
            <KonvaTimeline
                headerLabel='Исполнители'
                rowHeight={38}
                displayTasksLabel
                enableDrag={permission}
                enableResize={permission}
                dateLocale="ru"
                localized={{duration: 'Длительность', end: 'К', start: 'Н'}}
                timezone="Europe/Moscow"
                workIntervals={workIntervals}
                dragResolution={step}
                resolution={resolution}
                range={range}
                resources={resources}
                tasks={tasks}
                onErrors={onErrors}
                onTaskClick={onTaskClick}
                onTaskChange={(t) => setChangedTask(t)}
            />
            <Alerts/>
        </>
    );
};

export default Main;