const obj1 = {
  property1: "prop1"
}

const obj2 = Object.create(obj1);

obj2.ownProperty2 = "prop2";
obj2.ownProperty3 = "prop3";

function selfKeys(object) {
  for (let key in object) {
    if (object.hasOwnProperty(key)){
      console.log(`${key}: ${object[key]}`);
    }
  }
}


selfKeys(obj2)
