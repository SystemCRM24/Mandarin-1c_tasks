import React, { useCallback, useEffect } from "react";
import { 
    createContext, 
    useContext, 
    useState, 
    useMemo 
} from 'react';

import { getPermissions } from "../../api";
import useAfterDisplay from "../../hooks/useAfterDisplay";


const AppContext = createContext();


export const AppProvider = ({ children }) => {
    // Права пользователя 0 - права на просмотр
    const [permission, setPermission] = useState(null);
    useEffect(
        () => {
            const fetchPermission = async () => {
                const response = await getPermissions();
                setPermission(Boolean(response));
            };
            fetchPermission();
        },
        []
    );

    // Флаг загрузки
    const [isLoading, setIsLoading] = useState(true);

    // Флаг Синхронизации
    const [isSyncing, setIsSyncing] = useState(false);
    
    // Доступное Разрешение
    const viewResolutions = useMemo(
        () => {
            return {
                "1hrs": '1 час',
                "3hrs": '3 часа',
                "1day": '1 день'
            }
        }, 
        []
    );
    const _viewsKeys = Object.keys(viewResolutions);
    const defaultResolution = _viewsKeys[_viewsKeys.length - 1];
    const [resolution, setResolution] = useState(defaultResolution);

    // Доступные значения для drag и resize задач.
    const dragResolutions = useMemo(
        () => {
            return {
                "1min": '1 минута',
                "5min": '5 минут', 
                "10min": '10 минут', 
                "15min": '15 минут', 
                "30min": '30 минут', 
                "1hrs": '1 час', 
                "1day": '1 день', 
            }
        },
        []
    );
    const [step, setStep] = useState(Object.keys(dragResolutions)[1]);

    // Функция для скрола виджета к временному блоку равному сегодня.
    const scrollToNow = useCallback(
        () => {
            const konvaMain = document.querySelector('#konva-today');
            konvaMain.scrollLeft = konvaMain.getAttribute('today-x');
        },
        [] 
    );

    // Функция для глубинного сравнения
    const isEqual = useCallback((left, right) => JSON.stringify(left) === JSON.stringify(right), []);

    // Организация WebSocket-соединения
    const [wsConnection, setWSConnection] = useState(null);
    const [wsMessage, setWSMessage] = useState(null);
    useEffect(
        () => {
            const socket = new WebSocket("wss://office.ra-mandarin.com:444/v3/front/ws");
            socket.onopen = () => console.log('WebSocket connected');
            socket.onmessage = (event) => {
                console.log('Message received');
                setWSMessage(JSON.parse(event.data));
            };
            socket.onclose = () => {
                console.log('WebSocket disconnected');
                setWSMessage(null);
            };
            setWSConnection(socket);
            return () => socket.close();
        },
        []
    );

    // Переменные для Konva
    const [workIntervals, setWorkIntervals] = useState(null);
    const [range, setRange] = useState(null);
    const [resources, setResources] = useState(null);
    const [tasks, setTasks] = useState(null);
    const [errors, setErrors] = useState([]);

    // Отслеживание заполнение полей для отрисовки ганта
    useEffect(
        () => {
            const allResources = (
                permission !== null &&
                workIntervals !== null &&
                range !== null && 
                resources !== null &&
                tasks !== null
            );
            setIsLoading(!allResources);
        },
        [permission, workIntervals, range, resources, tasks, setIsLoading]
    );

    // Очистка ресурсов виджета при разрыве соединения
    const clearWidgetResources = useCallback(
        () => {
            setIsLoading(true);
            setPermission(null);
            setIsSyncing(false);
            // setWorkIntervals([]);
            setRange(null);
            setResources(null);
            setTasks(null);
            setErrors([]);
        },
        []
    );

    const handleRange = useCallback(
        (oldRange, newRange) => !isEqual(oldRange, newRange) && setRange(newRange),
        [setRange]
    );

    const handleWorkIntervals = useCallback(
        (oldIntervals, newIntervals) => !isEqual(oldIntervals, newIntervals) && setWorkIntervals(newIntervals),
        [setWorkIntervals]
    );

    const handleResources = useCallback(
        (oldResources, newResources) => {
            let department = null;
            let colorIndex = -1;
            const colors = [
                '#0d6efd',      // $blue
                '#fd7e14',      // $orange
                '#20c997',      // $teal
                '#6610f2',      // $indigo
                '#ffc107',      // $yellow
                '#198754',      // $green
                '#6f42c1',      // $purple
                '#0dcaf0'       // $cyan
            ];
            for ( const resource of newResources ) {
                if ( department !== resource.department ) {
                    department = resource.department;
                    colorIndex ++;
                }
                if ( colorIndex == colors.length ) {
                    colorIndex = 0;
                }
                resource.color = colors[colorIndex];
            }
            !isEqual(oldResources, newResources) && setResources(newResources);
        },
        [setResources]
    );

    const handleTasks = useCallback(
        (newTasks) => {
            for ( const task of newTasks ) {
                task.label = task.label.split(' ')[1];
                task.description = task.description.split('\n')[0].split(': ')[1]
                const time = task.time;
                time.start = Date.parse(time.start);
                time.end = Date.parse(time.end);
                task.deadline = Date.parse(task.deadline);
            }
            setTasks(newTasks);
        },
        [setTasks]
    );

    // Обработка сообщений от WebSocket
    useEffect(
        () => {
            const meta = wsMessage?.meta;
            const content = wsMessage?.content;
            switch ( meta ) {
                case "data":
                    handleRange(range, content.interval);
                    handleWorkIntervals(workIntervals, content.workIntervals);
                    handleResources(resources, content.resources);
                    handleTasks(content.tasks);
                    break;
                case "sync":
                    setIsSyncing(content);
                    break;
                default:
                    clearWidgetResources();
            }
        },
        [wsMessage]
    );

    // Хук на скролл при рендере Konva
    useAfterDisplay("konva-today", isLoading, scrollToNow);

    return (
        <AppContext.Provider
            value={{
                permission,
                isLoading,
                setIsLoading,
                isSyncing, 
                setIsSyncing,
                viewResolutions,
                resolution, 
                setResolution,
                dragResolutions,
                step, 
                setStep,
                scrollToNow,
                wsConnection,
                workIntervals,
                range,
                resources,
                tasks,
                setTasks,
                errors,
                setErrors
            }}
        >
            {children}
        </AppContext.Provider>
    );
};

export const useAppContext = () => useContext(AppContext);
