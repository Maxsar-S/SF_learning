function Appliance(power) {
  this.energy = 'electricity',
  this.place = 'cabinet',
  this.power = power
}

Appliance.prototype.powerSocket = function(powerSocket) {
  console.log(`Appliance uses power socket: ${powerSocket}`)
}


function ElectricAppliance(power, battery) {
  this.power = power;
  this.battery = battery;
}

ElectricAppliance.prototype = new Appliance();


const lamp = new ElectricAppliance(10, 'true');
lamp.powerSocket(false);
console.log(lamp);

const computer = new ElectricAppliance(100, 'false');
computer.powerSocket(true);
console.log(computer);
