import { 
    Button,
    ToggleButton,
    ButtonGroup,
    OverlayTrigger, 
    Tooltip,
    Form,
    Spinner
} from 'react-bootstrap';

import { useAppContext } from '../Context';
import './Header.css';


// const resolutions = {
//     "1min": '1 минута',
//     "5min": '5 минут', 
//     "10min": '10 минут', 
//     "15min": '15 минут', 
//     "30min": '30 минут', 
//     "1hrs": '1 час', 
//     "2hrs": '2 часа', 
//     "6hrs": '6 часов', 
//     "12hrs": '12 часов',
//     "1day": '1 день', 
//     "1week": '1 неделя', 
//     "2weeks": '2 недели'
// };


function HeaderWT({id, ttext, children}) {
    return (
        <OverlayTrigger
            overlay={
                <Tooltip id={id}>
                    {ttext}
                </Tooltip>
            }
            delay={{ show: 2000, hide: 0 }}
            placement='right'
        >
            <h5>{children}</h5>
        </OverlayTrigger>
    );
};


function Header() {
    const {
        viewResolutions,
        resolution,
        setResolution,
        dragResolutions,
        step,
        setStep,
        scrollToNow,
        isSyncing
    } = useAppContext();

    return (
        <div id="headerTop">
            <div id="headerSelects">
                <div>
                    <HeaderWT id='h0' ttext="Изменяет разрешение временной шкалы.">
                        Разрешение
                    </HeaderWT>
                    <ButtonGroup>
                        {Object.entries(viewResolutions).map(
                            ([key, value]) => (
                                <ToggleButton
                                    key={key}
                                    id={`radio-${key}`}
                                    type="radio"
                                    variant={resolution === key ? 'primary' : 'outline-dark'}
                                    name='radio'
                                    value={key}
                                    checked={resolution === key}
                                    onChange={(e) => setResolution(e.currentTarget.value)}
                                >
                                    {value}
                                </ToggleButton>
                            )
                        )}
                    </ButtonGroup>
                </div>
                <div>
                    <HeaderWT id='h1' ttext="Поле выбора шага округления времени задач при их изменении.">
                        Шаг
                    </HeaderWT>
                    <Form.Select onChange={(e) => setStep(e.target.value)}>
                        {Object.entries(dragResolutions).map(
                            ([key, value]) => {
                                return (
                                    <option key={key} value={key} selected={step === key}>
                                        {value}
                                    </option>
                                )
                            }
                        )}
                    </Form.Select>
                </div>
                <div id='nowBtn'>
                    <Button onClick={scrollToNow}>Сегодня</Button>
                </div>
            </div>
            <Spinner 
                hidden={!isSyncing}
                animation="grow" 
                variant="success"
            />
        </div>
    );
}

export default Header;