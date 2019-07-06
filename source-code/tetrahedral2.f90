! This is a second attempt at tetrahedral, doesn't work, more to come
! Maybe bug in vectors? Do math by hand tomorrow for errors, if not, no idea
! 0 is for Owen


program data_format
    implicit none
    integer :: nuse, nskip, narg, i, nframe, uz, ret, &
     natoms, istep, j, k, m, pnum, na, coordnum
    real :: time, gbox(3,3), prec, bin, ength, side, reff
    character (len = 256) :: fname, xtcfile, arg(50), outfile
    real, allocatable :: coord(:), diff(:), up(:), results(:,:)
    integer :: x, y, z, c1, c2, total, numone, t1, t2
    real :: pr, psize, dx, dy, dz, length, v, order, sigma, ang
    logical :: cave
    real :: dist(4), points(12), orders(21800), test_(2180), ab(3), bc(3)
    real :: a, b, c, temp, mval, mval2
    
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
                        t1 = 0
                        test_ = 10
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
                            t1 = t1 + 1
                            test_(t1) = length
                            !print *, minval(test_)
                            if(length < maxval(dist)) then
                                c2 = (maxloc(dist, DIM=1) - 1) * 3 + 1
                                dist(maxloc(dist)) = length
                                points(c2) = coord(m)
                                points(c2+1) = coord(m+1)
                                points(c2+2) = coord(m+2)
                            end if
                        end do
                        !print *, "DIST"
                        !do m = 1, 4
                        !    print *, minval(dist), minval(test_)
                        !    if (minval(dist) /= minval(test_)) read(*,*)
                        !    test_(minloc(test_)) = 10
                        !    dist(minloc(dist)) = 10
                        !end do
                        do m = 1, size(points)
                            results(c1, m+3) = points(m)
                        end do
                        sigma = 0
                        print *, "------------------------------------"
                        do i = 1, 9, 3
                            ! I know I am doing needless calculations, I merely do so for readability purposes
                            ab(1) = points(i) - results(c1, 1)
                            ab(2) = points(i + 1) - results(c1, 2)
                            ab(3) = points(i + 2) - results(c1, 3)
                            if (ab(1) > 0.5 * side) ab(1) = ab(1) - side
                            if (ab(2) > 0.5 * side) ab(2) = ab(2) - side
                            if (ab(3) > 0.5 * side) ab(3) = ab(3) - side
                            do j = i + 3, 12, 3
                                bc(1) = points(j) - results(c1, 1)
                                bc(2) = points(j + 1) - results(c1, 2)
                                bc(3) = points(j + 2) - results(c1, 3)
                                if (bc(1) > 0.5 * side) bc(1) = bc(1) - side
                                if (bc(2) > 0.5 * side) bc(2) = bc(2) - side
                                if (bc(3) > 0.5 * side) bc(3) = bc(3) - side
                                !print *, ab(1), ab(2), ab(3), bc(1), bc(2), bc(3)
                                ang = dot_product(ab, bc)
                                !print *, ang
                                ang = ang / ((sqrt(ab(1)**2 + ab(2)**2 + ab(3)**2)) * (sqrt(bc(1)**2 + bc(2)**2 + bc(3)**2)))
                                print *, "arrrr", acos(ang), results(c1, 1), results(c1, 2), results(c1, 3), points(i), &
                                points(i+1), points(i+2), points(j), points(j+1), points(j+2)
                                !read(*,*)
                                ang = (ang + 1/3)**2
                                sigma = sigma + ang 
                            end do
                        end do
                        !print *, 'sigma', sigma
                        order = 1 - 0.375 * sigma
                        !if (order < 0) then 
                        !    do m = 1, 15
                        !        print *, results(c1, m)
                        !    end do 
                        !end if
                        !print *, 'order', order
                        if (order < 0 .OR. order > 1) then
                            print *, order
                            read(*,*)
                        end if
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

    mval = 0
    mval2 = 1
    do i = 1, size(orders)
        if (orders(i) > mval) mval = orders(i)
        if (orders(i) < mval2) mval2 = orders(i)
    end do
    print *, mval, mval2
    print *, maxval(orders), minval(orders)
    do i = 1, size(orders) 
        !if (orders(i) < 0) print *, orders(i)
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
