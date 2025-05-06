import { AppProvider } from "./components/Context";
import Loading from "./components/Loading";


const App = () => {
    return (
        <AppProvider>
            <Loading/>
        </AppProvider>
    );
}

export default App;
