import { checkHealth } from "@/shared/api/health";
import { useEffect } from "react";

function App() {
  useEffect(() => {
    checkHealth().then(console.log).catch(console.error);
  }, []);

  return <h1>Welcome to Booking!</h1>;
}

export default App;
