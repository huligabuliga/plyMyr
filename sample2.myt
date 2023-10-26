program my_program;
vars
    int x, y, z[10];
end

main(){
    x = 10;
    y = 20;
    z[0] = x + y;
    z[1] = x - y;
    z[2] = x * y;
    z[3] = x / y;
    z[4] = x % y;
    z[5] = x == y;
    z[6] = x != y;
    z[7] = x < y;
    z[8] = x > y;
    z[9] = x <= y;
    z[10] = x >= y;
    write(z[0]);
    write(z[1]);
    write(z[2]);
    write(z[3]);
    write(z[4]);
    write(z[5]);
    write(z[6]);
    write(z[7]);
    write(z[8]);
    write(z[9]);
    write(z[10]);
}