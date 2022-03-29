# Simple satellite model

### System image

![System image](https://github.com/btcHehe/PyControl/blob/master/examples/satellite/img/system.png "system image")

### Block diagram

![block diagram image](https://github.com/btcHehe/PyControl/blob/master/examples/satellite/img/systemDiag.png "block diagram image")

### Parameters
* M(t) - Torque acting on satellite
* I - inertia of the satellite
* θ(t) - angle of the satellite relative to gravitational force which is perpendicular to planet surface

### Model building

Equations we are gonna use in model building:  
![basic equations](https://github.com/btcHehe/PyControl/blob/master/examples/satellite/img/1.png "basic equations")

Using Newton's Second Law for angular motion we can derive equations:  
![Newton's second law equations](https://github.com/btcHehe/PyControl/blob/master/examples/satellite/img/nsl.png "Newton's second law equations")

Assuming zero initial conditions we can derive transfer function for our object:  
![transfer function definition](https://github.com/btcHehe/PyControl/blob/master/examples/satellite/img/tf.png "transfer function definition")

General state space model:  
![alt text](https://github.com/btcHehe/PyControl/blob/master/examples/satellite/img/ss.png "state space equations")

Now we can define our state space variables as (our goal is to control output voltage):  
![alt text](https://github.com/btcHehe/PyControl/blob/master/examples/satellite/img/ssconv.png "state space convertion equations")

Finally we define state space model matrices as:  
![alt text](https://github.com/btcHehe/PyControl/blob/master/examples/satellite/img/mats.png "state space matrix definition")
