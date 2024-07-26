havoc y;
assume y >= 0;
c := 0;
r := y;
while c < y
inv c <= y and r = y * c and c>=0
do
{
r := r + y;
c := c + 1
};
assert r = y*y