
> Name

FMZ-Tutorial-JavaScript-Quick-Start-Manual

> Author

作手君TradeMan





> Source (javascript)

``` javascript
//In the textconsole.logAt/InFMZCan Be Used for DebuggingLogFunction Instead
// Commenting Method andCis similar, this is a single-line comment
/* This Is Multi-line
   Notes */

// Statements can end with a semicolon
doStuff();

// ... But semicolons can also be omitted; whenever a new line is encountered, a semicolon is automatically inserted (except in some special cases)).
doStuff()

// Because these special cases can lead to unexpected results, we leave the semicolon here.

///////////////////////////////////
// 1. Numbers, strings, and operators

// Javascript Only one numeric type(That is 64bit IEEE 754 Double-Precision Float double).
// double Yes 52 bits represent the decimal, enough to accurately store values up to 9✕10¹⁵ Integer of.
3; // = 3
1.5; // = 1.5

// all basic arithmetic operations work as you expect.
1 + 1; // = 2
0.1 + 0.2; // = 0.30000000000000004
8 - 1; // = 7
10 * 2; // = 20
35 / 5; // = 7

// Includes division that cannot be evenly divided.
5 / 2; // = 2.5

// bit operations are the same as in other languages; When you perform bitwise operations on floating-point numbers,
// Floating-point numbers will be converted to*at most* 32 bit unsigned integers.
1 << 2; // = 4

// Parentheses can determine precedence.
(1 + 3) * 2; // = 8

// There are three non-numeric numeric types
Infinity; // 1/0 Result of
-Infinity; // -1/0 Result of
NaN; // 0/0 Result of

// Also Has Boolean Value.
true;
false;

// Strings can be constructed using single or double quotes.
'abc';
"Hello, world";

// Use ! to Negate
!true; // = false
!false; // = true

// equal ===
1 === 1; // = true
2 === 1; // = false

// No wait !=
1 !== 1; // = false
2 !== 1; // = true

// More comparison operators 
1 < 10; // = true
1 > 10; // = false
2 <= 2; // = true
2 >= 2; // = true

// Used for String+Connect
"Hello " + "world!"; // = "Hello world!"

// Strings can also be used < ,> To compare
"a" < "b"; // = true

// Use"=="Type conversion occurs when comparing...
"5" == 5; // = true
null == undefined; // = true

// ...Unless You Are Using ===
"5" === 5; // = false
null === undefined; // = false 

// ...But can lead to strange behavior
13 + !0; // 14
"13" + !0; // '13true'

// You Can Use`charAt`To get characters in a string
"This is a string".charAt(0);  // = 'T'

// ...Or use `substring` To get a larger portion.
"Hello world".substring(0, 5); // = "Hello"

// `length` It's a property, so do not use it ().
"Hello".length; // = 5

// There are two special values:`null`and`undefined`
null;      // is used to represent intentionally set null values.
undefined; // is used to represent a value that has not yet been set (although `undefined` itself is actually a value)

// false, null, undefined, NaN, 0 and "" are false; all others are considered logically true
// NOTE 0 Is Falsy  "0"is logically true, although 0 == "0".

///////////////////////////////////
// 2. Variables, arrays, and objects

// Variables Need to Use`var`Keyword declaration.Javascriptis a dynamically typed language,
// So you don't need to specify the type. Assignment requires `=` 
var someVar = 5;

// If you don't add when declaringvarKeyword, and you won't get an error...
someOtherVar = 10;

// ...However, at this point, this variable will be created in the global scope, not in the current scope you define

// variables that are not assigned will be set toundefined
var someThirdVar; // = undefined

// There are some shorthand ways to perform mathematical operations on variables:
someVar += 5; // Equivalent to someVar = someVar + 5; someVar It is now 10 
someVar *= 10; // Now someVar is 100

// Increment and decrement also have shorthand
someVar++; // someVar Yes/Is 101
someVar--; // Return 100

// an array is an ordered list composed of elements of any type
var myArray = ["Hello", 45, true];

// Elements of the array can be accessed using bracket indices.
// Array index starts from0Start.
myArray[1]; // = 45

// The array is mutable and has variables length.
myArray.push("World");
myArray.length; // = 4

// Add at the specified index/Modify
myArray[3] = "Hello";

// javascriptThe object in is equivalent to an"Dictionary"Or"Mapping":is the key-Unordered collection of key-value pairs.
var myObj = {key1: "Hello", key2: "World"};

// Keys are strings, but if the key itself is validjsidentifier in other languages, so quotation marks are not required.
// Values can be of any type.
var myObj = {myKey: "myValue", "my other key": 4};

// Object properties can be accessed via subscript
myObj["my other key"]; // = 4

// ... Or you can also use . ,If the attribute is a legal identifier
myObj.myKey; // = "myValue"

// The object is mutable; values can also be changed or new keys can be added
myObj.myThirdKey = true;

// If you want to obtain a value that has not been defined yet, it will returnundefined
myObj.myFourthKey; // = undefined

///////////////////////////////////
// 3. Logical and control structures

// The syntax introduced in this section is related toJavaSyntax is almost identical

// `if`Statements are the same as in other languages.
var count = 1;
if (count == 3){
    // count Yes/Is 3 Execute at
} else if (count == 4){
    // count Yes/Is 4 Execute at
} else {
    // Execute in other cases 
}

// whileLoop
while (true) {
    // Infinite loop
}

// Do-while and While Loop is very similar to , but it will be executed at least once
var input;
do {
    input = getInput();
} while (!isValid(input))

// `for`Loops andC,JavaSame as in:
// Initialize; Conditions for continuing execution; Iteration.
for (var i = 0; i < 5; i++){
    // Iterate5times
}

// && Is logical AND, || Is logical OR
if (house.size == "big" && house.colour == "blue"){
    house.contains = "bear";
}
if (colour == "red" || colour == "blue"){
    // colourYes/IsredorblueExecute at
}

// && and || Yes/Is"Short circuit"statement, which is particularly useful when setting initialization values 
var name = otherName || "default";

// `switch`Statement usage`===`Check equality.
// In eachcaseUse at the end 'break'
// Otherwise, what followscaseStatements will also be executed. 
grade = 'B';
switch (grade) {
  case 'A':
    console.log("Great job");
    break;
  case 'B':
    console.log("OK job");
    break;
  case 'C':
    console.log("You can do better");
    break;
  default:
    console.log("Oy vey");
    break;
}

///////////////////////////////////
// 4. Functions, scope, closures

// JavaScript Function by`function`Keyword definition
function myFunction(thing){
    return thing.toUpperCase();
}
myFunction("foo"); // = "FOO"

// Note that the returned value must start with`return`The line with the keyword,
// Otherwise due to automatic semicolon completion, you will return`undefined`.
// In useAllmanPay attention to style.
function myFunction()
{
    return // <- Semicolons are automatically inserted here
    {
        thisIsAn: 'object literal'
    }
}
myFunction(); // = undefined

// javascriptIn the middle, functions are first-class objects, so functions can also be assigned to a variable,
// And are passed as arguments -- For example, an event handler function:
function myFunction(){
    // This piece of code will be executed in5seconds
}
setTimeout(myFunction, 5000);
// NOTE:setTimeoutNojsis part of the language, but instead provided by the browser andNode.jsProvided.

// Function objects do not even need to declare a name -- You can directly write a function definition into the parameter of another function
setTimeout(function(){
    // This piece of code will be executed in5seconds
}, 5000);

// JavaScript Has function scope; Functions have their own scope, while other code blocks do not.
if (true){
    var i = 5;
}
i; // = 5 - is not what we expect in other languagesundefined

// This leads to people often using"Immediately-invoked anonymous function"Pattern of,
// This can prevent some temporary variables from leaking into the global scope.
(function(){
    var temporary = 5;
    // We can access and modify the global object("global object")To access the global scope,
    // At/InwebIn the browser is`window`This object. 
    // In other environments such asNode.jsThe name of this object in may vary.
    window.permanent = 10;
})();
temporary; // Throw a reference exceptionReferenceError
permanent; // = 10

// javascriptOne of the most powerful features is closures.
// If a function is defined within another function, then the inner function has access to all variables of the outer function.,
// Even after the external function ends.
function sayHelloInFiveSeconds(name){
    var prompt = "Hello, " + name + "!";
    // Internal functions are by default placed in local scope,
    // Just like using`var`Declared.
    function inner(){
        alert(prompt);
    }
    setTimeout(inner, 5000);
    // setTimeoutis asynchronous, so sayHelloInFiveSeconds The function will exit immediately,
    // And setTimeout Will be called laterinner
    // However, becauseinneris made bysayHelloInFiveSeconds"Closed inclusion"of,
    // Soinnerstill accessible when it is finally called`prompt`Variables.
}
sayHelloInFiveSeconds("Adam"); // Will pop up after 5 seconds "Hello, Adam!"


///////////////////////////////////
// 5. Objects, constructors, and prototypes

//  Objects can contain methods.
var myObj = {
    myFunc: function(){
        return "Hello world!";
    }
};
myObj.myFunc(); // = "Hello world!"

// When the function in the object is called, this function can through`this`Keyword accesses the object it is attached to.
myObj = {
    myString: "Hello world!",
    myFunc: function(){
        return this.myString;
    }
};
myObj.myFunc(); // = "Hello world!"

// But this function actually accesses its runtime environment, not the definition-time environment, depending on how the function is called.
// So if the function is called outside the context of this object, it will not run successfully.
var myFunc = myObj.myFunc;
myFunc(); // = undefined

// Accordingly, a function can also be specified as a method of an object and can be used as a method`this`Visit
// Members of this object, even if they are not attached to the object when the function is defined.
var myOtherFunc = function(){
    return this.myString.toUpperCase();
}
myObj.myOtherFunc = myOtherFunc;
myObj.myOtherFunc(); // = "HELLO WORLD!"

// When we go through`call`or`apply`When calling a function, you can also specify an execution context for it.
var anotherFunc = function(s){
    return this.myString + s;
}
anotherFunc.call(myObj, " And Hello Moon!"); // = "Hello World! And Hello Moon!"

// `apply`The function is almost exactly the same, only requiring onearrayTo pass the argument list.
anotherFunc.apply(myObj, [" And Hello Sun!"]); // = "Hello World! And Hello Sun!"

// When a function accepts a series of parameters and you want to pass in aarrayParticularly useful when.
Math.min(42, 6, 27); // = 6
Math.min([42, 6, 27]); // = NaN (uh-oh!)
Math.min.apply(Math, [42, 6, 27]); // = 6

// But`call`and`apply`This is just temporary. If we want the function to attach to an object, we can use`bind`.
var boundFunc = anotherFunc.bind(myObj);
boundFunc(" And Hello Saturn!"); // = "Hello World! And Hello Saturn!"

// `bind` Can also be used for partial application of a function (currying)).
var product = function(a, b){ return a * b; }
var doubler = product.bind(this, 2);
doubler(8); // = 16

// When you pass through`new`When the keyword calls a function, an object is created,
// And can be accessed throughthisKeyword to access this function.
// A function designed to be called this way is called a constructor.
var MyConstructor = function(){
    this.myNumber = 5;
}
myNewObj = new MyConstructor(); // = {myNumber: 5}
myNewObj.myNumber; // = 5
```

> Detail

https://www.fmz.com/strategy/395725

> Last Modified

2023-01-16 09:43:09
