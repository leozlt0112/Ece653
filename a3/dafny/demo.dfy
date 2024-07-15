method Abs(x: int) returns (y: int)
  ensures y >= 0;
  ensures x>= 0 ==> y ==x
  ensures x< 0 ==> y ==-x

{
  if (x < 0) {
    return -x;
  } else {
    return x;
  }

}

method Testing()
{
  var v := Abs(-3);
  assert 0<= v;
  assert v ==3;
}

method MultipleReturns(x: int, y: int) returns (more: int, less:int)
  requires !(y<0)
  ensures less <=x <=more
{
  more := x+y;
  less := x-y;

}