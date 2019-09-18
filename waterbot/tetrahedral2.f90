
program data_format
    implicit none
    integer :: nuse, nskip, narg, i, nframe, uz, ret, &
     natoms, istep, j, k, m, pnum, na, coordnum
    real :: time, gbox(3,3), prec, bin, ength, side, reff
    character (len = 256) :: fname, xtcfile, arg(50), outfile
    real, allocatable :: coord(:), diff(:), up(:), results(:), orders(:)
    real, allocatable :: distrib(:)
    integer :: x, y, z, c1, c2, total, numone, c3
    real :: pr, psize, dx, dy, dz, length, v, order, sigma, ang
    logical :: cave
    real :: dist(4), points(12), ab(3), bc(3)
    real :: a, b, c, temp
    
    side = 5 ! Side length of box
    nuse = 10 ! Number of frames to use
    pnum = 4142 ! Number of particles
    na = 3
    nskip = 0
    bin = 0.01
    xtcfile = 'ccni.xtc' ! Input file
    outfile = 'tetra.dat' ! Output file
    print *, "Beginning formatting"

    allocate(distrib(int(1/bin)))
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
                                c2 = (maxloc(dist, DIM=1) - 1) * 3 + 1
                                dist(maxloc(dist)) = length
                                points(c2) = coord(m)
                                points(c2+1) = coord(m+1)
                                points(c2+2) = coord(m+2)
                            end if
                        end do
                        sigma = 0
			do i = 1, 9, 3
                            ! I know I am doing needless calculations, I merely do so for readability purposes
                            dx = abs(coord(k) - points(i))
                            dy = abs(coord(k+1) - points(i + 1))
                            dz = abs(coord(k+2) - points(i + 2))
                            if (dx > 0.5 * side) then
				if (coord(k) - points(i) > 0) points(i) = points(i) + side
				if (coord(k) - points(i) < 0) points(i) = points(i) - side
			    end if
                            if (dy > 0.5 * side) then
				if (coord(k+1) - points(i+1) > 0) points(i+1) = points(i+1) + side
				if (coord(k+1) - points(i+1) < 0) points(i+1) = points(i+1) - side 
			    end if
                            if (dz > 0.5 * side) then
				if (coord(k+2) - points(i+2) > 0) points(i+2) = points(i+2) + side
				if (coord(k+2) - points(i+2) < 0) points(i+2) = points(i+2) - side
			    end if
			    ab(1) = coord(k) - points(i)
                            ab(2) = coord(k + 1) - points(i+1)
			    ab(3) = coord(k + 2) - points(i+2)
                            do j = i + 3, 12, 3
                                dx = abs(coord(k) - points(j))
                                dy = abs(coord(k+1) - points(j + 1))
                                dz = abs(coord(k+2) - points(j + 2))
                                if (dx > 0.5 * side) then
				    if (coord(k) - points(j) > 0) points(j) = points(j) + side
				    if (coord(k) - points(j) < 0) points(j) = points(j) - side
				end if
                                if (dy > 0.5 * side) then
				    if (coord(k+1) - points(j+1) > 0) points(j+1) = points(j+1) + side
				    if (coord(k+1) - points(j+1) < 0) points(j+1) = points(j+1) - side
				end if
                                if (dz > 0.5 * side) then
				    if (coord(k+2) - points(j+2) > 0) points(j+2) = points(j+2) + side
				    if (coord(k+2) - points(j+2) < 0) points(j+2) = points(j+2) - side
				end if
				bc(1) = coord(j) - coord(k)
                                bc(2) = coord(j + 1) - coord(k+1)
				bc(3) = coord(j + 2) - coord(k+2)
                                !print *, ab(1), ab(2), ab(3), bc(1), bc(2), bc(3)
                                ang = ab(1)*bc(1)+ab(2)*bc(2)+ab(3)*bc(3)
                                !print *, ang
                                ang = ang / (sqrt(ab(1)**2 + ab(2)**2 + ab(3)**2) * sqrt(bc(1)**2 + bc(2)**2 + bc(3)**2))
                                !print *, "arrrr", acos(ang), results(c1, 1), results(c1, 2), results(c1, 3), points(i), &
                                !points(i+1), points(i+2), points(j), points(j+1), points(j+2)
                                !read(*,*)
                                ang = (ang + 1.0/3.0)**2
                                sigma = sigma + ang 
                            end do
			end do
                        !print *, 'sigma', sigma
                        order = 1 - 3.0/8.0 * sigma
                        !if (order < 0) then 
                        !    do m = 1, 15
                        !        print *, results(c1, m)
                        !    end do 
                        !end if
                        !print *, 'order', order
                        c3 = floor(order/bin)+1
                        !distrib(c3) = distrib(c3) + 1
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
    do i = 1, int(1/bin)
        write(10,*) i, distrib(i)
    end do

    write(*,*) ' '
    write(*,*) 'Done'
    write(*,*) ' '
    
end program data_format
