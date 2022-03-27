# Simple DC motor model

### System image

![alt text](https://github.com/btcHehe/PyControl/tree/master/examples/DCengine/img/system.png "system image")

### Block diagram

![alt text](https://github.com/btcHehe/PyControl/tree/master/examples/DCengine/img/systemDiag.png "block diagram image")

### Parameters
* U(t) - input voltage
* R - motor coil resistance
* L - motor coil inductance
* i(t) - current flowing in circuit
* Vemf - electromotive force acting on motor 
* Ke - motor electromotive constant
* Km - motor torque constant
* Il - load inertia (assume that shaft inertia is negligible)
* ω(t) - angular velocity of engine shaft/load

### Model building

Equations we are gonna use in model building:
![alt text](https://github.com/btcHehe/PyControl/tree/master/examples/DCengine/img/1.png "basic equations")

Using Kirchhoff's Voltage Law we can derive equations:
![alt text](https://github.com/btcHehe/PyControl/tree/master/examples/DCengine/img/KVL.png "KVL equations")

From mechanics we can derive torque equations:
![alt text](https://github.com/btcHehe/PyControl/tree/master/examples/DCengine/img/torque.png "torque equations")

General state space model:
![alt text](https://github.com/btcHehe/PyControl/tree/master/examples/DCengine/img/ss.png "state space equations")

Now we can define our state space variables as (our goal is to control angular velocity):
![alt text](https://github.com/btcHehe/PyControl/tree/master/examples/DCengine/img/ssconv.png "state space convertion equations")

Finally we define state space model matrices as:
![alt text](https://github.com/btcHehe/PyControl/tree/master/examples/DCengine/img/mats.png "state space matrix definition")


