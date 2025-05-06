import Spinner from 'react-bootstrap/Spinner';
import './Loading.css';

import Main from '../Main';
import { useAppContext } from '../Context';


function Loading() {
    const { isLoading } = useAppContext();
    return (
        isLoading 
        ?
        <Spinner id="Loading" animation="grow" role="status" variant='primary'>
            <span className="visually-hidden">Loading...</span>
        </Spinner>
        :
        <Main/>
    )
}

export default Loading;