import { onMounted } from "vue";
import { toast } from "vue-sonner";



export function useWebSocket(url) {
    let ws = null;
    onMounted(() => {

        if (ws) return; // singleton guard

        try {

            ws = new WebSocket(url);

            ws.onmessage = ({ data }) => {
                toast.info(data);
            };

            ws.onerror = (err) => {
                console.error("WebSocket error:", err);
            };

            ws.onclose = () => {
                console.log("WebSocket closed");
                ws = null;
            };
        } catch (err) {
            console.error("WebSocket init failed:", err);
        }
    });

    return { ws };
}