
> Name

Grid-Management-Tool

> Author

program

> Strategy Description

**GridPriceManagerUsed to create and manage the grid list, store grid orders**

### Initialize

| Parameter | Required | Description                                        |
| ----------- | -------- | ------------------------------------------- |
| upper_price | NO       | Upper boundary price of the grid                              |
| lower_price | NO       | Lower boundary price of the grid                              |
| grid_num    | NO       | Number of grids (arithmetic progression)                              |
| interval    | NO       | Grid interval (geometric)                              |
| side        | NO       | Supports passing `long`, `short`, defaults if not filled in`long` |
| Data        | NO       | Grid information already exists, type is dictionary                    |

```python
# creates an arithmetic grid with prices between 1000 and 800, and quantities of 10
GridPriceManager(upper_price=1000, lower_price=800, grid_num=10)

# Created a geometric grid with prices ranging from 1000 to 800, spaced at 1% intervals
GridPriceManager(upper_price=1000, lower_price=800, interval=1)

# Pass in existing grid information
data = {
	"grid_list":    {99:None,100:None,101:None,102:None,103:None,104:None},
	"interval":     None,
	"upper_price":  104,
	"lower_price":  99,
	"grid_num":     6,
	"side":         "long",
	"grid_diff":    1,
	"type":         "Equal differences",
}
GridPriceManager(Data=data)
```

### DataStructure

| Parameter | Required | Description                                                       |
| ----------- | -------- | ---------------------------------------------------------- |
| grid_list   | YES      | Grid price and order information are stored as key-value pairs, with key as price and value as orderid |
| interval    | YES      |                                                            |
| upper_price | YES      |                                                            |
| lower_price | YES      |                                                            |
| grid_num    | YES      |                                                            |
| side        | YES      |                                                            |
| grid_diff   | YES      |                                                            |
| type        | YES      | Arithmetic or geometric                                               |

### Function

+ get_nearest_buy_price(current_price)

  **Get the latest grid buy price**

  | Parameter | Required | Description                                 |
  | ------------- | -------- | ------------------------------------ |
  | current_price | YES      | Pass in the price to find the nearest buying price based on this price |

+ get_nearest_sell_price(current_price)

  **Get the latest grid sell price**

  | Parameter | Required | Description                                 |
  | ------------- | -------- | ------------------------------------ |
  | current_price | YES      | Pass in the price to find the nearest selling price based on this price |

+ base_position(ticker)

  **Bottom warehouse**

  | Parameter | Required | Description                                                         |
  | ------ | -------- | ------------------------------------------------------------ |
  | ticker | YES      | Open the bottom position to open the grid. This function will execute the callback function `event` event`base_position` |

+ add_order(order_id)

  **Add upper and lower grid orders**

  | Parameter | Required | Description                                                         |
  | -------- | -------- | ------------------------------------------------------------ |
  | order_id | YES      | Add grid upper and lower pending orders. Pass in the id function of the bottom position or transaction order to find the upper and lower grids of this id. This function will execute the callback function `event` event.`add_order` |

+ cancel_order(order_id)

  **Cancel order**

  | Parameter | Required | Description                                                        |
  | -------- | -------- | ----------------------------------------------------------- |
  | order_id | YES      | Revoke a specified order; this function executes the callback function 'event' event`cancel_order` |

### Event

Event refers to the specified callback function called during function execution. Here, the event function is always used to pass in the specified event. Decorator mode

```python
gm = GridPriceManager(1000, 800, 10)

# Bottom position event, this event will be triggered when the base_position method is called
@gm.event('base_position')
def base_position(price):
    # Pass in the latest grid price and use this price as a reference for buying price
    print(price)
    return 123456	# Return base order,mangerrecord the order
```

| Event | Is it required | Pass in | Return                                               |
| ------------- | -------- | ------------------------------------------------------------ | -------------------------------------------------- |
| base_position | YES      | price,Buying price, float type | bottom position orderid                                         |
| add_order     | NO       | price,Buying grid price, dict type, {"up": upper grid price, "down": lower grid price} | A dict with the same format as the one passed in, corresponding to the upper grid transaction ID and the lower grid transactionid |
| cancel_order  | NO       | order_id,Specify the canceled order id, int or str type | bool, whether the cancellation is successful                                 |
| change        | NO       | grid_list                                                    | Grid information changes trigger this event                         |





> Source (python)

``` python
class GridPriceManager:
    def __init__(self, Data=None, upper_price=None, lower_price=None, interval=None, grid_num=None, side: Literal['long','short']='long') -> dict:
        self.interval = interval
        self.upper_price = upper_price
        self.lower_price = lower_price
        self.grid_num = grid_num
        self.side = side
        self.grid_diff = None
        self.type = None    # Grid type
        if self.grid_num is not None:
            self.grid_diff = (self.upper_price - self.lower_price) / (self.grid_num - 1)
        if Data is None: 
            if self.interval is None:
                self.grid_list = self._generate_grid_list_difference()
                self.type = "Equal differences"
            else:
                self.grid_list = self._generate_grids_list_ratio()
                self.type = "Equal ratio"
        else:
            self.grid_list = Data["grid_list"]
            self.interval = Data["interval"]
            self.upper_price = Data["upper_price"]
            self.lower_price = Data["lower_price"]
            self.grid_num = Data["grid_num"]
            self.side = Data["side"]
            self.grid_diff = Data["grid_diff"]
            self.type = Data["type"]
        self.data = f"Grid type: {self.type}, number of grids: {len(self.grid_list)}, upper and lower range: [{self.upper_price}-{self.lower_price}, direction: {self.side}]"
        self.callback = {}

    def event(self, event_name):
        """Event"""
        def decorator(func):
            self.callback[event_name] = func
            return func
        return decorator

    def _generate_grid_list_difference(self) -> dict:
        """Arithmetic Grid Generation"""
        grid_list = {}
        price = self.lower_price
        for _ in range(self.grid_num):
            grid_list[price] = None
            price += self.grid_diff
        grid_list[self.upper_price] = None
        return grid_list

    def _generate_grids_list_ratio(self) -> dict:
        """Geometric Grid Generation"""
        ratio = 1 + self.interval / 100
        grid = [self.lower_price * (ratio ** i) for i in range(-100, 101)]
        return {round(g, 8): None for g in grid if self.lower_price <= g <= self.upper_price}


    def get_nearest_buy_price(self, current_price) -> float:
        """Get the latest grid buy price"""
        nearest_price = None
        for price in sorted(self.grid_list.keys()):
            if price > current_price:
                break
            nearest_price = price
        return nearest_price

    def get_nearest_sell_price(self, current_price) -> float:
        """Get the latest grid sell price"""
        nearest_price = None
        for price in sorted(self.grid_list.keys(), reverse=True):
            if price < current_price:
                break
            nearest_price = price
        return nearest_price
    
    def base_position(self, ticker) -> Union[str, int]:
        """Bottom warehouse"""
        if self.side == "short":
            t = self.get_nearest_sell_price(ticker)
        else:
            t = self.get_nearest_buy_price(ticker)
        order_id = self.callback["base_position"](t)
        self.grid_list[t] = order_id
        self.callback["change"](self.grid_list)
        return order_id
    
    def add_order(self, order_id) -> Union[Dict, bool]:
        """Add upper and lower grid orders"""
        up_price = None
        down_price = None
        ticker = None
        keys = list(self.grid_list.keys())
        for i in range(len(keys)-1):
            if self.grid_list[keys[i]] == order_id:
                ticker = keys[i]
                try:
                    if self.side is None or self.side == "long":
                        up_price = keys[i+1]
                        down_price = keys[i-1]
                    else:
                        up_price = keys[i-1]
                        down_price = keys[i+1]
                except IndexError:
                    return False
                break

        PriceDict = {"up": up_price, "down": down_price}
        d = self.callback["add_order"](PriceDict)
        d = {"up": d["up"], "down": d["down"]}
        self.grid_list[up_price] = d["up"]
        self.grid_list[down_price] = d["down"]
        self.grid_list[ticker] = None
        self.callback["change"](self.grid_list)
        return d
    
    def cancel_order(self, order_id):
        """Cancel order"""
        result = self.callback["cancel_order"](order_id)
        if result == True:
            for items in self.grid_list.items():
                if items[1] == order_id:
                    self.grid_list[items[0]] = None
                    self.callback["change"](self.grid_list)
                    break

def main():
    gm = GridPriceManager(1000, 500, 10)

    @gm.event('add_order')
    def add_order(price):
        print(price)
        return {
            'up': 36543,
            'down': 87957,
        }

    @gm.event('cancel_order')
    def cancel_order(order_id):
        return True

    @gm.event('base_position')
    def base_position(price):
        print(price)
        return 123456

    a = gm.base_position(600)
    print(a)
    a = gm.add_order(123456)
    print(gm.grid_list)
    gm.cancel_order(87957)
    print(gm.grid_list)
```

> Detail

https://www.fmz.com/strategy/411935

> Last Modified

2023-05-01 12:32:46
