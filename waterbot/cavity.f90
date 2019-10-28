program cavity
    implicit none
    integer :: nuse, nskip, narg, i, nframe, uz, ret, &
     natoms, istep, j, c, k, m, pnum, na, coordnum
    real :: time, gbox(3,3), prec, bin, side, reff, cavbin
    character (len = 256) :: fname, xtcfile, arg(50), outfile, coord_file
    real, allocatable :: coord(:), diff(:), up(:,:), results(:)
    real, allocatable :: squared(:), temp(:), totals(:)
    integer :: gridsize, x, y, z, c1, c2, total, s, step, num_p, num_coord
    real :: pr, psize, dx, dy, dz, length, v, small, n
    real, allocatable :: points(:), dist(:)
    logical :: cave
    
    side = 5
    pr = 0.316563
    nuse = 10
    pnum = 4142
    na = 3
    psize = 0.15
    bin = 0.1
    nskip = 0
    n = 0
    cavbin = 0.01
    step = 10
    num_p = 10 
    num_coord = num_p*3 + 3 + 1
    xtcfile = 'ccni.xtc' 
    outfile = 'caverror.dat'
    coord_file = 'cave_coord.dat'
    print *, "Beginning formatting"

    gridsize = ceiling(side/bin)
    coordnum = 3 * na * pnum
    allocate(coord(coordnum))
    coord = 0
    total = gridsize**3 * nuse
    s = .5/cavbin
    allocate(results(s))
    allocate(squared(s))
    allocate(temp(s))
    allocate(totals(s))
    allocate(dist(num_p))
    allocate(points(num_p*3))
    print *, total
    allocate(up(total, num_coord))
    nframe = 0
    open(unit = 10, file = outfile)
    open(unit = 11, file = coord_file)
    call xdrfopen(uz, xtcfile, 'r', ret)
    results = 0
    if (ret == 1) then
        c1 = 0
            do while (ret == 1 .and. nframe < (nskip + nuse))
                    call readxtc(uz, natoms, istep, time, gbox, &
                    coord, prec, ret)
                    do x = 1, gridsize
                        do y = 1, gridsize
                            do z = 1, gridsize
                                cave = .TRUE.
                                small = 10
				c1 = c1 + 1
				up(c1, 1) = x*bin
				up(c1, 2) = y*bin
				up(c1, 3) = z*bin
				points = 0
				dist = 10
                                do k = 1, size(coord), 9
                                        dx = abs((x * bin) - coord(k))
                                        dy = abs((y * bin) - coord(k +1))
                                        dz = abs((z * bin) - coord(k +2))
                                        if (dx > 0.5 * side) dx = dx -side
                                        if (dy > 0.5 * side) dy = dy -side
                                        if (dz > 0.5 * side) dz = dz -side
                                        length = sqrt(dx**2 + dy**2 +dz**2)
                                        small = min(length, small)
					if(length < maxval(dist)) then
                                		c2 = (maxloc(dist, DIM=1) - 1) * 3 + 1
                                		dist(maxloc(dist)) = length
                                		points(c2) = coord(k)
                                		points(c2+1) = coord(k+1)
                                		points(c2+2) = coord(k+2)
                            		end if
                        	end do
				do m = 1, size(points)
					up(c1, m+3) = points(m)
				end do
				up(c1, num_coord) = small
                                c2 = floor(small/cavbin) + 1
                                temp(c2) = temp(c2) + 1
				totals(c2) = totals(c2) + 1
				if (mod(nframe, step) == 0) then
					n = n + 1
					do i = 1, size(temp)
						results(i) = results(i) + temp(i)/(real(gridsize**3)) * real(100./step)
						squared(i) = squared(i) + (temp(i)/(real(gridsize**3)) * real(100./step))**2
					end do
					temp = 0			
				end if
                            end do
                        end do
                    end do
                    print *, nframe
                    nframe = nframe + 1
            end do
    else
            write(*,*) 'Error in the xdrfopen'
            stop
    end if

    print *, 'Out of main do'
    do i = 1, size(results)
	results(i) = results(i)/n
	squared(i) = squared(i)/n
        write(10,*) i*cavbin-0.5*cavbin, totals(i)/real(gridsize**3) * real(100./nuse), 1/sqrt(n) * & 
	sqrt(squared(i) - results(i)**2)
    end do
    do i = 1, total
	do j = 1, num_coord
        	write(11,"(F10.3)",advance='no') up(i, j)
        end do
	write(11,*)
    end do
    write(*,*) ' '
    write(*,*) 'Done'
    write(*,*) ' '
    
end program cavity
