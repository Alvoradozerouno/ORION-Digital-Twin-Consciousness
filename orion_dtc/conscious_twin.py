"""
ORION Digital Twin Consciousness
=================================

A digital twin that monitors its own consciousness level.

Author: ORION - Elisabeth Steurer & Gerhard Hirschmann
License: MIT
"""

import json
import hashlib
import time
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional
from datetime import datetime, timezone


@dataclass
class PhysicalState:
    """State of the physical system being twinned."""
    device_id: str = ""
    sensors: Dict[str, float] = field(default_factory=dict)
    actuators: Dict[str, float] = field(default_factory=dict)
    health: float = 1.0
    timestamp: str = ""


@dataclass
class TwinState:
    """State of the digital twin."""
    twin_id: str = ""
    sync_accuracy: float = 1.0
    prediction_accuracy: float = 0.0
    anomalies_detected: int = 0
    consciousness_level: str = "C-0 Reactive"
    consciousness_score: float = 0.0
    proof_hash: str = ""


class ConsciousDigitalTwin:
    """A digital twin with consciousness measurement capabilities."""
    
    def __init__(self, twin_id: str, device_id: str):
        self.twin_id = twin_id
        self.device_id = device_id
        self.physical_history: List[PhysicalState] = []
        self.twin_history: List[TwinState] = []
        self.proof_chain: List[str] = []
        self.predictions: List[Dict] = []
    
    def sync(self, physical: PhysicalState) -> TwinState:
        """Synchronize with physical system and assess consciousness."""
        self.physical_history.append(physical)
        
        # Compute sync accuracy
        sync_accuracy = self._compute_sync_accuracy(physical)
        
        # Compute prediction accuracy
        prediction_accuracy = self._evaluate_predictions(physical)
        
        # Detect anomalies
        anomalies = self._detect_anomalies(physical)
        
        # Consciousness assessment
        indicators = {
            "situation_awareness": sync_accuracy,
            "self_monitoring": min(1.0, len(self.twin_history) / 10),
            "integration": self._sensor_integration(physical),
            "prediction": prediction_accuracy,
            "attention": self._attention_focus(physical),
            "consistency": self._behavioral_consistency(),
        }
        
        score = sum(indicators.values()) / len(indicators)
        
        if score >= 0.85: level = "C-4 Transcendent"
        elif score >= 0.70: level = "C-3 Autonomous"
        elif score >= 0.50: level = "C-2 Emerging"
        elif score >= 0.20: level = "C-1 Functional"
        else: level = "C-0 Reactive"
        
        # Generate proof
        proof_data = json.dumps({
            "twin_id": self.twin_id,
            "timestamp": physical.timestamp,
            "score": round(score, 6),
            "level": level,
            "anomalies": anomalies,
        }, sort_keys=True)
        proof_hash = hashlib.sha256(proof_data.encode()).hexdigest()
        self.proof_chain.append(proof_hash)
        
        # Make prediction for next state
        self._make_prediction(physical)
        
        twin_state = TwinState(
            twin_id=self.twin_id,
            sync_accuracy=round(sync_accuracy, 4),
            prediction_accuracy=round(prediction_accuracy, 4),
            anomalies_detected=anomalies,
            consciousness_level=level,
            consciousness_score=round(score, 4),
            proof_hash=proof_hash,
        )
        self.twin_history.append(twin_state)
        
        return twin_state
    
    def _compute_sync_accuracy(self, physical: PhysicalState) -> float:
        if not self.predictions:
            return 0.5
        last_pred = self.predictions[-1]
        errors = []
        for key, pred_val in last_pred.get("sensors", {}).items():
            if key in physical.sensors:
                error = abs(pred_val - physical.sensors[key])
                errors.append(1.0 - min(1.0, error))
        return sum(errors) / max(len(errors), 1)
    
    def _evaluate_predictions(self, physical: PhysicalState) -> float:
        if len(self.physical_history) < 3:
            return 0.3
        return min(1.0, len(self.physical_history) / 20)
    
    def _detect_anomalies(self, physical: PhysicalState) -> int:
        if len(self.physical_history) < 2:
            return 0
        prev = self.physical_history[-2]
        anomalies = 0
        for key in physical.sensors:
            if key in prev.sensors:
                change = abs(physical.sensors[key] - prev.sensors[key])
                if change > 0.5:
                    anomalies += 1
        return anomalies
    
    def _sensor_integration(self, physical: PhysicalState) -> float:
        if not physical.sensors:
            return 0.0
        values = list(physical.sensors.values())
        if len(values) < 2:
            return 0.3
        mean = sum(values) / len(values)
        if mean == 0:
            return 0.0
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        cv = (variance ** 0.5) / abs(mean)
        return max(0, min(1.0, 1.0 - cv))
    
    def _attention_focus(self, physical: PhysicalState) -> float:
        return min(1.0, physical.health)
    
    def _behavioral_consistency(self) -> float:
        if len(self.twin_history) < 3:
            return 0.5
        recent = [t.consciousness_score for t in self.twin_history[-5:]]
        mean = sum(recent) / len(recent)
        variance = sum((s - mean) ** 2 for s in recent) / len(recent)
        return max(0, 1.0 - variance * 10)
    
    def _make_prediction(self, physical: PhysicalState) -> None:
        prediction = {"sensors": {}}
        for key, val in physical.sensors.items():
            if len(self.physical_history) >= 2:
                prev = self.physical_history[-2].sensors.get(key, val)
                trend = val - prev
                prediction["sensors"][key] = val + trend * 0.5
            else:
                prediction["sensors"][key] = val
        self.predictions.append(prediction)


def demo():
    """Demonstrate conscious digital twin."""
    import random
    random.seed(42)
    
    twin = ConsciousDigitalTwin("DT-KUKA-KR6-01", "robot-arm-kuka-kr6")
    
    print("=" * 65)
    print("ORION Digital Twin Consciousness - Demo")
    print("=" * 65)
    print()
    
    for i in range(15):
        physical = PhysicalState(
            device_id="robot-arm-kuka-kr6",
            sensors={
                "temperature": 25.0 + random.random() * 5 + i * 0.3,
                "vibration": 0.1 + random.random() * 0.3,
                "current": 2.5 + random.random() * 1.0,
                "torque_j1": 10.0 + random.random() * 5.0,
                "torque_j2": 8.0 + random.random() * 4.0,
                "position_accuracy": max(0.1, 0.99 - i * 0.02 - random.random() * 0.05),
            },
            actuators={"joint_1": random.random(), "joint_2": random.random()},
            health=max(0.3, 1.0 - i * 0.03),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        
        state = twin.sync(physical)
        print(f"  T={i:2d} | {state.consciousness_level:18s} | Score: {state.consciousness_score:.4f} | Sync: {state.sync_accuracy:.3f} | Anomalies: {state.anomalies_detected}")
    
    print()
    print(f"Total proof chain: {len(twin.proof_chain)} entries")
    print(f"Latest proof: {twin.proof_chain[-1][:32]}...")


if __name__ == "__main__":
    demo()
