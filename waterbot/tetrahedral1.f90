program data_format
    implicit none
    integer :: nuse, nskip, narg, i, nframe, uz, ret, &
     natoms, istep, j, k, m, pnum, na, coordnum
    real :: time, gbox(3,3), prec, bin, ength, side, reff
    character (len = 256) :: fname, xtcfile, arg(50), outfile
    real, allocatable :: coord(:), diff(:), up(:), results(:), orders(:)
    real, allocatable :: distrib(:), squared(:)
    integer :: x, y, z, c1, c2, total, numone, c3
    real :: pr, psize, dx, dy, dz, length, v, order, sigma, ang
    logical :: cave
    real :: dist(4), points(12)
    real :: a, b, c, temp
    
    side = 5 ! Side length of box
    nuse = 50 ! Number of frames to use
    pnum = 4142 ! Number of particles
    na = 3
    nskip = 0
    bin = 0.01
    xtcfile = 'ccni2.xtc' ! Input file
    outfile = 'tetraerror.dat' ! Output file
    print *, "Beginning formatting"

    allocate(distrib(int(2/bin)))
    allocate(squared(int(2/bin)))
    squared = 0
    distrib = 0
    coordnum = 3 * na * pnum
    allocate(coord(coordnum)) ! Coordinates to be read in
    coord = 0
    total = pnum * nuse
    allocate(orders(total))
    allocate(results(total)) ! The output, the starting coordinate and the 4 other coordinates, with the final one being the order paramter
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
                    !do k = 1, 3
                    !	do j = 1, 3
                    !		print *, gbox(k,j)
                    !	end do
                    !end do
                    do k = 1, size(coord), 9
                        points = 0
                        dist = 10
                        c1 = c1 + 1
                        do m = 1, size(coord), 9
                            if (m == k) cycle
                            dx = abs(coord(k) - coord(m))
                            dy = abs(coord(k+1) - coord(m + 1))
                            dz = abs(coord(k+2) - coord(m + 2))
                            if (dx > 0.5 * side) dx = dx - side
                            if (dy > 0.5 * side) dy = dy - side
                            if (dz > 0.5 * side) dz = dz - side
                            length = sqrt(dx**2 + dy**2 + dz**2)
                            if(length < maxval(dist)) then
                                !print *, maxloc(dist)
                                c2 = (maxloc(dist, DIM=1) - 1) * 3 + 1
                                dist(maxloc(dist)) = length
                                points(c2) = coord(m)
                                points(c2+1) = coord(m+1)
                                points(c2+2) = coord(m+2)
                            end if
                        end do
                        sigma = 0
                        do i = 1, 9, 3
                            do j = i + 3, 12, 3
                                dx = abs(coord(k) - points(i))
                                dy = abs(coord(k+1) - points(i + 1))
                                dz = abs(coord(k+2) - points(i + 2))
                                if (dx > 0.5 * side) then
                                    dx = dx - side
                                    if (coord(k) - points(i) > 0) points(i) = points(i) + side
                                    if (coord(k) - points(i) < 0) points(i) = points(i) - side
                                end if
                                if (dy > 0.5 * side) then
                                    dy = dy - side
                                    if (coord(k+1) - points(i+1) > 0) points(i+1) = points(i+1) + side
                                    if (coord(k+1) - points(i+1) < 0) points(i+1) = points(i+1) - side
                                end if
                                if (dz > 0.5 * side) then
                                    dz = dz - side
                                    if (coord(k+2) - points(i+2) > 0) points(i+2) = points(i+2) + side
                                    if (coord(k+2) - points(i+2) < 0) points(i+2) = points(i+2) - side
                                end if
                                a = sqrt(dx**2 + dy**2 + dz**2)
                                dx = abs(coord(k) - points(j))
                                dy = abs(coord(k+1) - points(j + 1))
                                dz = abs(coord(k+2) - points(j + 2))
                                if (dx > 0.5 * side) then
                                    dx = dx - side
                                    if (coord(k) - points(j) > 0) points(j) = points(j) + side
                                    if (coord(k) - points(j) < 0) points(j) = points(j) - side
                                end if
                                if (dy > 0.5 * side) then
                                    dy = dy - side
                                    if (coord(k+1) - points(j+1) > 0) points(j+1) = points(j+1) + side
                                    if (coord(k+1) - points(j+1) < 0) points(j+1) = points(j+1) - side
                                end if
                                if (dz > 0.5 * side) then
                                    dz = dz - side
                                    if (coord(k+2) - points(j+2) > 0) points(j+2) = points(j+2) + side
                                    if (coord(k+2) - points(j+2) < 0) points(j+2) = points(j+2) - side
                                end if
                                b = sqrt(dx**2 + dy**2 + dz**2)
                                dx = abs(points(i) - points(j))
                                dy = abs(points(i + 1) - points(j + 1))
                                dz = abs(points(i + 2) - points(j + 2))
                                if (dx > 0.5 * side) dx = dx - side
                                if (dy > 0.5 * side) dy = dy - side
                                if (dz > 0.5 * side) dz = dz - side
                                c = sqrt(dx**2 + dy**2 + dz**2)
                                ang = real(c**2 - a**2 - b**2) / real(-2 * a *b)
                                !ang = acos(ang)
                                !print *, 'ang', ang
                                !if (ang >= 0.7) then
                                !    print *, ang
                                !    print *, coord(k), coord(k+1), coord(k+2)
                                !    print *, points(i), points(i+1), points(i+2)
                                !    print *, points(j), points(j+1), points(j+2)
                                !end if
                                ang = (ang + 1.0/3.0)**2
                                !if (ang > 1.5) print *, ang
                                sigma = sigma + ang
                            end do
                        end do
                        !print *, 'sigma', sigma
                        order = 1 - 3.0/8.0 * sigma
                        !if (order < 0) then 
                        !    print *, order
                        !    print *, coord(k), coord(k+1), coord(k+2)
                        !    do m = 1, 12, 3
                        !        print *, points(m), points(m+1), points(m+2)
                        !    end do 
                        !end if
                        !print *, 'order', order
                        c3 = floor((order+1)/bin)+1
                        distrib(c3) = distrib(c3) + 1
			squared(c3) = squared(c3) + 1
                        orders(c1) = order
                        results(c1) = order
                    end do
                    print *, nframe
                    nframe = nframe + 1
            end do
    else
            write(*,*) 'Error in the xdrfopen'
            stop
    end if

    print *, maxval(orders), minval(orders)
        ! These prints are used for debugging
    numone = 0
    do i = 1, size(orders) 
        if (orders(i) < 0) numone = numone + 1 !print *, orders(i)
    end do
    print *, numone
        ! Write to the file
    do i = 1, int(2/bin)
	squared(i) = squared(i)**2
        write(10,*) (i-1)*bin-1-0.5*bin, real(distrib(i))/real(pnum)*(100./nuse), sqrt((squared(i)/real(pnum)*(100./nuse)) &
	 - (distrib(i)/real(pnum)*real(100./nuse))**2) * 1/sqrt(real(nuse))
    end do

    write(*,*) ' '
    write(*,*) 'Done'
    write(*,*) ' '
    
end program data_format
