# ─────────────────────────────────────────────────────────────
# MESSAGING LAYER — message_bus.py
# A simple beginner-friendly message queue in Python
# No external libraries needed — uses Python's built-in queue
#
# Think of it like a mailbox:
#   - Services PUT messages in
#   - Other services TAKE messages out
#
# Run: python message_bus.py
# ─────────────────────────────────────────────────────────────

import queue       # Python's built-in thread-safe queue
import threading   # For running things at the same time
import time        # For timestamps and delays
import json        # For formatting messages nicely

# ─────────────────────────────────────────────────────────────
# 1. THE MESSAGE BUS
#    This is like a post office. Anyone can drop off a message.
#    Anyone can pick one up.
# ─────────────────────────────────────────────────────────────

class MessageBus:
    def __init__(self):
        # A dictionary of topic → queue
        # Example topics: "order.placed", "user.registered"
        self.topics = {}
        self.lock = threading.Lock()

    def get_or_create_topic(self, topic):
        """Create a new topic (mailbox) if it doesn't exist yet."""
        with self.lock:
            if topic not in self.topics:
                self.topics[topic] = queue.Queue()
                print(f"  [BUS] New topic created: '{topic}'")
        return self.topics[topic]

    def publish(self, topic, message):
        """
        PUBLISH = drop a message into a topic.
        Like putting a letter in the mailbox.
        """
        q = self.get_or_create_topic(topic)
        event = {
            "topic":     topic,
            "message":   message,
            "timestamp": time.strftime("%H:%M:%S"),
        }
        q.put(event)
        print(f"\n  📤 PUBLISHED to '{topic}': {json.dumps(message)}")

    def consume(self, topic, timeout=2):
        """
        CONSUME = pick up a message from a topic.
        Like taking a letter out of the mailbox.
        Returns None if there's nothing to read after 'timeout' seconds.
        """
        q = self.get_or_create_topic(topic)
        try:
            return q.get(timeout=timeout)
        except queue.Empty:
            return None  # No messages right now, that's okay!

    def pending_count(self, topic):
        """How many messages are waiting in a topic?"""
        q = self.get_or_create_topic(topic)
        return q.qsize()


# ─────────────────────────────────────────────────────────────
# 2. EXAMPLE SERVICES (producers and consumers)
#    These simulate what your real microservices would do.
# ─────────────────────────────────────────────────────────────

# Create ONE shared bus that all services use
bus = MessageBus()


def order_service_producer():
    """
    ORDER SERVICE (Producer)
    Publishes a message every time an order is placed.
    """
    print("\n--- Order Service: placing orders ---")
    orders = [
        {"order_id": 1, "customer": "Alice", "total": 299.99, "items": ["Laptop bag"]},
        {"order_id": 2, "customer": "Bob",   "total": 49.50,  "items": ["USB cable", "Mouse"]},
        {"order_id": 3, "customer": "Carol",  "total": 1200.0, "items": ["Monitor"]},
    ]
    for order in orders:
        bus.publish("order.placed", order)
        time.sleep(1)  # Wait 1 second between orders


def notification_service_consumer():
    """
    NOTIFICATION SERVICE (Consumer)
    Listens for 'order.placed' and sends a notification.
    """
    print("\n--- Notification Service: listening for orders ---")
    while True:
        event = bus.consume("order.placed", timeout=3)
        if event is None:
            print("  [Notif] No more messages. Stopping.")
            break
        order = event["message"]
        print(f"  📧 [Notif] Sending email to {order['customer']}: "
              f"Your order #{order['order_id']} (₱{order['total']}) is confirmed!")


def inventory_service_consumer():
    """
    INVENTORY SERVICE (Consumer)
    Also listens on 'order.placed' to update stock.
    Note: In a real bus (like Kafka), multiple consumers
    can read the SAME message independently.
    Here we simulate this with a slight delay.
    """
    print("\n--- Inventory Service: listening for orders ---")
    time.sleep(0.5)  # Slight delay so it reads after notif service
    while True:
        event = bus.consume("order.placed", timeout=3)
        if event is None:
            print("  [Inventory] No more messages. Stopping.")
            break
        order = event["message"]
        items = ", ".join(order["items"])
        print(f"  📦 [Inventory] Reducing stock for: {items}")


# ─────────────────────────────────────────────────────────────
# 3. RUN EVERYTHING
#    Threads let producers and consumers run "at the same time"
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  MESSAGING LAYER — Simple Python Message Bus")
    print("  Topics act like channels/mailboxes for events")
    print("=" * 55)

    # Start producer and consumers in separate threads
    producer  = threading.Thread(target=order_service_producer,      name="OrderService")
    consumer1 = threading.Thread(target=notification_service_consumer, name="NotifService")
    consumer2 = threading.Thread(target=inventory_service_consumer,    name="InventoryService")

    producer.start()
    consumer1.start()
    consumer2.start()

    # Wait for all threads to finish
    producer.join()
    consumer1.join()
    consumer2.join()

    print("\n" + "=" * 55)
    print("  All messages processed! Bus is empty.")
    print("=" * 55)
