import { onMounted } from "vue";
import { toast } from "vue-sonner";

let ws = null;

export function useWebSocket(url) {
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