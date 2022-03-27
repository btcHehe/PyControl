# Simple electronic circuit

### System image

![alt text](https://github.com/btcHehe/PyControl/tree/master/examples/electronics/img/system.png "system image")

### Block diagram

![alt text](https://github.com/btcHehe/PyControl/tree/master/examples/electronics/img/systemDiag.png "block diagram image")

### Parameters
* Uin(t) - input voltage 
* R - resistance
* L - inductance
* C - capacitance
* i(t) - current flowing in circuit
* Uc(t) - voltage on capacitor (output voltage also)

### Model building

Equations we are gonna use in model building:
![alt text](https://github.com/btcHehe/PyControl/tree/master/examples/electronics/img/1.png "basic equations")

Using Kirchhoff's Voltage Law we can derive equations:
![alt text](https://github.com/btcHehe/PyControl/tree/master/examples/electronics/img/KVL.png "KVL equations")

Assuming zero initial conditions we can derive transfer function for our object:
![alt text](https://github.com/btcHehe/PyControl/tree/master/examples/electronics/img/tf.png "transfer function definition")

General state space model:
![alt text](https://github.com/btcHehe/PyControl/tree/master/examples/electronics/img/ss.png "state space equations")

Now we can define our state space variables as (our goal is to control output voltage):
![alt text](https://github.com/btcHehe/PyControl/tree/master/examples/electronics/img/ssconv.png "state space convertion equations")

Finally we define state space model matrices as:
![alt text](https://github.com/btcHehe/PyControl/tree/master/examples/electronics/img/mats.png "state space matrix definition")

