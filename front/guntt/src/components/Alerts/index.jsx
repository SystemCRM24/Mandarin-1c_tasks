import Alert from 'react-bootstrap/Alert';


import "./Alerts.css";
import { useAppContext } from '../Context';


const BASE = "https://office.ra-mandarin.com";
const TASKPATH = '/workgroups/group/1/tasks/task/view/';


export default function Alerts() {
    const { errors, tasks } = useAppContext();

    return (
        <div id="alerts">
            {errors.map((alert => {
                if ( alert.entity === 'task' ) {
                    let errorTask = null;
                    for ( const task of tasks ) {
                        if ( task.id == alert.refId ) {
                            errorTask = task;
                            break;
                        }
                    }
                    const uri = `${BASE}${TASKPATH}${errorTask.id}/`;
                    return (
                        <Alert key={errorTask.id} variant={'danger'}>
                            Ошибка отрисовки задачи: 
                            <Alert.Link href={uri} target='_blank'>
                                {errorTask.label}
                            </Alert.Link>
                            . level: {alert.level}; message: {alert.message}
                        </Alert>
                    )
                }
            }))}
        </div>
    );
}
