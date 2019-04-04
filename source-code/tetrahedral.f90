! 0 is for Owen

! Minimum value is -0.16 (still below 0)
program data_format
    implicit none
    integer :: nuse, nskip, narg, i, nframe, uz, ret, &
     natoms, istep, j, k, m, pnum, na, coordnum
    real :: time, gbox(3,3), prec, bin, ength, side, reff
    character (len = 256) :: fname, xtcfile, arg(50), outfile
    real, allocatable :: coord(:), diff(:), up(:), results(:,:)
    integer :: x, y, z, c1, c2, total, numone
    real :: pr, psize, dx, dy, dz, length, v, order, sigma, ang
    logical :: cave
    real :: dist(4), points(12), orders(21800)
    real :: a, b, c, temp
    
    side = 4
    nuse = 10
    pnum = 2180
    na = 3
    nskip = 0
    xtcfile = 'traj.xtc' 
    outfile = 'tetra.dat'
    print *, "Beginning formatting"


    coordnum = 3 * na * pnum
    allocate(coord(coordnum))
    coord = 0
    total = pnum * nuse
    allocate(results(total, 16))
    nframe = 0
    numone = 0
    open(unit = 10, file = outfile)
    print *, total
    call xdrfopen(uz, xtcfile, 'r', ret)
    if (ret == 1) then
        c1 = 0
            do while (ret == 1 .and. nframe < (nskip + nuse))
                    call readxtc(uz, natoms, istep, time, gbox, &
                    coord, prec, ret)
                    do k = 1, size(coord), 9
                        points = 0
                        dist = 10
                        c1 = c1 + 1
                        results(c1, 1) = coord(k)
                        results(c1, 2) = coord(k+1)
                        results(c1, 3) = coord(k+2)
                        do m = 1, size(coord), 9
                            if (m == k) cycle
                            dx = abs(results(c1, 1) - coord(m))
                            dy = abs(results(c1, 2) - coord(m + 1))
                            dz = abs(results(c1, 3) - coord(m + 2))
                            if (dx > 0.5 * side) dx = dx - side
                            if (dy > 0.5 * side) dy = dy - side
                            if (dz > 0.5 * side) dz = dz - side
                            length = sqrt(dx**2 + dy**2 + dz**2)
                            if(length < maxval(dist)) then
                                c2 = (maxloc(dist, DIM=1) - 1) * 3 + 1
                                dist(maxloc(dist)) = length
                                points(c2) = coord(m)
                                points(c2+1) = coord(m+1)
                                points(c2+2) = coord(m+2)
                            end if
                        end do
                        do m = 1, size(points)
                            results(c1, m+3) = points(m)
                        end do
                        sigma = 0
                        do i = 1, 9, 3
                            ! I know I am doing needless calculations, I merely do so for readability purposes
                            do j = i + 3, 12, 3
                                dx = abs(results(c1, 1) - points(i))
                                dy = abs(results(c1, 2) - points(i + 1))
                                dz = abs(results(c1, 3) - points(i + 2))
                                if (dx > 0.5 * side) dx = dx - side
                                if (dy > 0.5 * side) dy = dy - side
                                if (dz > 0.5 * side) dz = dz - side
                                a = sqrt(dx**2 + dy**2 + dz**2)
                                dx = abs(results(c1, 1) - points(j))
                                dy = abs(results(c1, 2) - points(j + 1))
                                dz = abs(results(c1, 3) - points(j + 2))
                                if (dx > 0.5 * side) dx = dx - side
                                if (dy > 0.5 * side) dy = dy - side
                                if (dz > 0.5 * side) dz = dz - side
                                b = sqrt(dx**2 + dy**2 + dz**2)
                                dx = abs(points(i) - points(j))
                                dy = abs(points(i + 1) - points(j + 1))
                                dz = abs(points(i + 2) - points(j + 2))
                                if (dx > 0.5 * side) dx = dx - side
                                if (dy > 0.5 * side) dy = dy - side
                                if (dz > 0.5 * side) dz = dz - side
                                c = sqrt(dx**2 + dy**2 + dz**2)
                                ang = (c**2 - a**2 - b**2) / (-2 * a * b)
                                ang = acos(ang)
                                !print *, 'ang', ang
                                ang = (cos(ang) + 1/3)**2
                                sigma = sigma + ang
                            end do
                        end do
                        !print *, 'sigma', sigma
                        order = 1 - 0.375 * sigma
                        !print *, 'order', order
                        orders(c1) = order
                        results(c1, 16) = order
                    end do
            print *, nframe
            nframe = nframe + 1
            end do
    else
            write(*,*) 'Error in the xdrfopen'
            stop
    end if

    print *, maxval(orders), minval(orders)
    do i = 1, size(orders) 
        if (orders(i) < 0) print *, orders(i)
    end do
    do i = 1, total
            do j = 1, 16
                write(10,"(F10.3)",advance='no') results(i, j)
            end do
            write(10,*)
    end do

    write(*,*) ' '
    write(*,*) 'Done'
    write(*,*) ' '
    
end program data_format   
