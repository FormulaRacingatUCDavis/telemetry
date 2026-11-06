import "clsx";
import { w as writable } from "./index.js";
import mqtt from "mqtt";
const client = writable(null);
const mqttDataNum = writable({});
const mqttDataStr = writable({});
const mqttClient = mqtt.connect("ws://192.168.137.172:9001");
client.set(mqttClient);
mqttClient.on("connect", () => {
  console.log("[MQTT] Connected to broker.");
  mqttClient.subscribe("can/frame");
  mqttClient.subscribe("can/log/status");
  mqttClient.subscribe("camera/log/status");
});
mqttClient.on("message", (topic, message) => {
  let msg;
  try {
    msg = JSON.parse(message.toString());
  } catch (err) {
    console.error("[MQTT] Bad JSON:", message.toString());
    return;
  }
  if (topic === "can/log/status") {
    mqttDataStr.update((data) => ({
      ...data,
      logStatus: msg.status,
      logReq: msg.status === "on" ? "Stop Log" : "Start Log",
      timestamp: msg.timestamp
    }));
  } else if (topic === "camera/log/status") {
    mqttDataStr.update((data) => ({
      ...data,
      recStatus: msg.status,
      recReq: msg.status === "on" ? "Stop Camera" : "Record Camera",
      timestamp: msg.timestamp
    }));
  } else if (topic === "can/frame") {
    switch (msg.id) {
      case 160: {
        mqttDataNum.update((data) => ({
          ...data,
          moduleTempA: msg.inv_module_a_temp,
          moduleTempB: msg.inv_module_b_temp,
          moduleTempC: msg.inv_module_c_temp,
          timestamp: msg.timestamp
        }));
        break;
      }
      case 1894: {
        mqttDataStr.update((data) => ({
          ...data,
          vcuState: msg.dashboard_state,
          timestamp: msg.timestamp
        }));
        break;
      }
      case 896: {
        mqttDataStr.update((data) => ({
          ...data,
          bmsState: msg.pei_bms_status,
          timestamp: msg.timestamp
        }));
        break;
      }
      case 171: {
        mqttDataStr.update((data) => ({
          ...data,
          mcState: msg.inv_run_fault !== "Normal" ? msg.inv_run_fault : msg.inv_post_fault,
          timestamp: msg.timestamp
        }));
        break;
      }
      case 192: {
        mqttDataNum.update((data) => ({
          ...data,
          dashboard_torque: msg.dashboard_torque,
          timestamp: msg.timestamp
        }));
        break;
      }
      case 165: {
        mqttDataNum.update((data) => ({
          ...data,
          inv_motor_speed: msg.inv_motor_speed,
          timestamp: msg.timestamp
        }));
        break;
      }
      case 897: {
        mqttDataNum.update((data) => ({ ...data, pei_soc: msg.pei_soc, timestamp: msg.timestamp }));
        break;
      }
    }
  }
});
export {
  mqttDataStr as m
};
