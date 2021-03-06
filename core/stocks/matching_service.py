from doctest import DocFileSuite
from .models import Portfolio,IncompleteOrder,CompleteOrder,Order
from queue import Queue
from threading import Lock, Condition, Thread


class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class MatchingService(metaclass=SingletonMeta):
    """
    Matching Service Singleton Caller
    """
    order_queue = Queue()
    order_queue_lock = Lock()
    order_ready = Condition()

    def __init__(self) -> None:
        self.worker = Thread(target=self.execute_method)
        self.worker.start()

    def enqueue_order(self, order):
        with self.order_queue_lock:
            self.order_queue.put(order)
        with self.order_ready:
            self.order_ready.notify()

    def execute_method(self):
        while True:
            with self.order_ready:
                self.order_ready.wait()
            with self.order_queue_lock:
                order = self.order_queue.get()
            matching_service(order)

#compra
def matching_service_buy(order,relevant_orders):
    buyer = order.client_dni
    try:
        buyer_portfolio = Portfolio.objects.get(client_dni = buyer, company_ruc = order.company_ruc)
    except Portfolio.DoesNotExist:
        buyer_portfolio = Portfolio.objects.create(client_dni = buyer,company_ruc=order.company_ruc,quantity= 0)

    total_sold = 0
    total_quantity = 0
    matched = False
    
    if order.quantity_left == 0:
        return

    for current_order in relevant_orders:  	
        seller = current_order.client_dni
        seller_portfolio = Portfolio.objects.get(client_dni = seller, company_ruc = current_order.company_ruc)
        quantity_sold = min(order.quantity_left, current_order.quantity_left)
        price = current_order.price

        if buyer.money < quantity_sold * price:
            break

        current_total_sold = (current_order.quantity - current_order.quantity_left) * current_order.avg_price
        current_total_sold += quantity_sold * price

        seller_total_sold = seller_portfolio.quantity * seller_portfolio.avg_price
        buyer_total_sold = buyer_portfolio.quantity * buyer_portfolio.avg_price

        current_order.quantity_left -= quantity_sold
        seller_portfolio.quantity -= quantity_sold
        buyer_portfolio.quantity += quantity_sold
        order.quantity_left -= quantity_sold
        current_order.avg_price = current_total_sold / (current_order.quantity - current_order.quantity_left)
        # print(order.quantity_left,quantity_sold,"\n\n\n\n\n")

        seller_total_sold -= quantity_sold * price
        buyer_total_sold += quantity_sold * price
        buyer_portfolio.avg_price = buyer_total_sold / buyer_portfolio.quantity

        buyer.money -= quantity_sold * price
        seller.money += quantity_sold * price
        total_sold += quantity_sold * price
        total_quantity += quantity_sold
        matched = True
    
        if current_order.quantity_left == 0:
            IncompleteOrder.objects.filter(pk = current_order.id).delete()
            CompleteOrder.objects.create(order_id=current_order)
        

        if seller_portfolio.quantity != 0:
            # seller_portfolio.avg_price = seller_total_sold / seller_portfolio.quantity
            seller_portfolio.save()
        else:
            seller_portfolio.delete()

        current_order.save()
        seller.save()
        buyer_portfolio.save()
        order.save()

        if order.quantity_left == 0:
            IncompleteOrder.objects.filter(pk = order.id).delete()
            CompleteOrder.objects.create(order_id=order)
            break

    if matched:
        order.company_ruc.latest_price = price
        order.company_ruc.save()


    if total_quantity > 0:
        order.avg_price = total_sold / total_quantity
    buyer.save()
    order.save()




#ventas
def matching_service_sell(order,relevant_orders):
    seller = order.client_dni
    total_bought = 0
    total_quantity = 0
    matched = False

    try:
        seller_portfolio = Portfolio.objects.get(client_dni = seller, company_ruc = order.company_ruc)
    except Portfolio.DoesNotExist:
        seller_portfolio = Portfolio.objects.create(client_dni = seller,company_ruc=order.company_ruc,quantity= 0)

    if order.quantity_left == 0:
        return
    
    for current_order in relevant_orders:  	
        buyer = current_order.client_dni
        buyer_portfolio = Portfolio.objects.get(client_dni = buyer, company_ruc = current_order.company_ruc)
        quantity_sold = min(order.quantity_left, current_order.quantity_left)
        price = current_order.price

        if buyer.money < quantity_sold * price:
            continue	
            #break

        current_total_sold = (current_order.quantity - current_order.quantity_left) * current_order.avg_price
        current_total_sold += quantity_sold * price

        seller_total_sold = seller_portfolio.quantity * seller_portfolio.avg_price
        buyer_total_sold = buyer_portfolio.quantity * buyer_portfolio.avg_price

        current_order.quantity_left -= quantity_sold
        seller_portfolio.quantity -= quantity_sold
        buyer_portfolio.quantity += quantity_sold
        order.quantity_left -= quantity_sold
        current_order.avg_price = current_total_sold / (current_order.quantity - current_order.quantity_left)

        seller_total_sold -= quantity_sold * price
        
        buyer_total_sold += quantity_sold * price
        buyer_portfolio.avg_price = buyer_total_sold / buyer_portfolio.quantity

        buyer.money -= quantity_sold * price
        seller.money += quantity_sold * price
        total_bought += quantity_sold * price
        total_quantity += quantity_sold
        matched = True
    
        if current_order.quantity_left == 0:
            IncompleteOrder.objects.filter(pk = current_order.id).delete()
            CompleteOrder.objects.create(order_id=current_order)
        

        if seller_portfolio.quantity != 0:
            seller_portfolio.save()
        else:
            seller_portfolio.delete()

        current_order.save()
        seller.save()
        buyer_portfolio.save()
        order.save()

        if order.quantity_left == 0:
            IncompleteOrder.objects.filter(pk = order.id).delete()
            CompleteOrder.objects.create(order_id=order)
            break

    if matched:
        order.company_ruc.latest_price = price
        order.company_ruc.save()

    if total_quantity > 0:
        order.avg_price = total_bought / total_quantity
    seller.save()
    order.save()


def matching_service(order):

    pending_orders_id = IncompleteOrder.objects.filter(status = IncompleteOrder.OrderStatus.PENDING)
    pending_orders = Order.objects.filter(id__in = pending_orders_id)

    company_orders = pending_orders.filter(company_ruc = order.company_ruc_id).exclude(client_dni_id = order.client_dni_id).exclude( transaction_type__startswith = order.transaction_type[0])
    if order.transaction_type[0] == 'B':  # compra 
        company_orders = company_orders.filter(price__lte = order.price).order_by("price","date")
        matching_service_buy(order,company_orders)
    elif order.transaction_type[0] == 'S':	# venta
        company_orders = company_orders.filter(price__gte = order.price).order_by("-price","date")
        matching_service_sell(order,company_orders)



