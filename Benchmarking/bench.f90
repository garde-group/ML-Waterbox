! 0 is for Owen

program benchmark
    implicit none
    integer :: results(12052), i, j, ones, zeros
    real :: coord(12052,64), reff, temp(63), dx, dy, dz, len
    real :: t1, t2, total

    reff = 0.23328

    open(unit=2, file="bf.dat")
    do i = 1, 12052
        do j = 1, 64
            read(2,*) coord(i, j)
        end do 
    end do 
    call cpu_time(t1)
    do i = 1, 12052
        do j = 4, 61, 3
            dx = abs(coord(i, 1) - coord(i, j))
            dy = abs(coord(i, 2) - coord(i, j+1))
            dz = abs(coord(i, 3) - coord(i, j+2))
            len = sqrt(dx**2 + dy**2 + dz**2)
            if (len < reff) then 
                results(i) = 0
                exit
            else if (j == 61) then
                results(i) = 1
            end if
        end do
    end do
    call cpu_time(t2)

    total = t2 - t1
    ones = 0
    zeros = 0
    do i = 1, 12052
        if (results(i) == 0) then
            zeros = zeros + 1
        else if (results(i) == 1) then
            ones = ones + 1
        end if
    end do

    print *, "Num 0: ", zeros, "Num 1: ", ones
    print *, "Time: ", total


end program benchmark
