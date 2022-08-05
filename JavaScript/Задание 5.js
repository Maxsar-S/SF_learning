class Appliance {
  constructor(power) {
    this.power = power;
    this.energy = 'electricity';
    this.place = 'cabinet';
  }
  getInfo() {
   return`Appliance use energy of ${this.energy}. Power of the electrical appliance is ${this.power} w.\
   Place to use: ${this.place}.`;
  }
}


class ElectrAppliance extends Appliance {
  constructor(powerSocket, battery, power) {
    super(power);
    this.powerSocket = powerSocket;
    this.battery = battery;
  }
  
  getInfo(){
    return(`Appliance use energy of ${this.energy}.\
    If battery - ${this.battery}, power socket is ${this.powerSocket} or in conversly.\
    Power of the electrical appliance is ${this.power} w. Place to use: ${this.place}.`)
  }
}

const lamp = new ElectrAppliance(false, true, 10);
console.log(lamp.getInfo());

const computer = new ElectrAppliance(true, false, 1000);
console.log(computer.getInfo());

console.log(computer instanceof ElectrAppliance);

