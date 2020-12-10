! I just whipped this up, so it's pretty rough and ready. 
! 0 is for Owen


program data_format
    implicit none
    integer :: nuse, nskip, narg, i, nframe, uz, ret, &
     natoms, istep, j, c, k, m, pnum, na, coordnum
    real :: time, gbox(3,3), prec, bin, side, reff, cavbin
    character (len = 256) :: fname, xtcfile, arg(50), outfile
    real, allocatable :: coord(:), diff(:), up(:), results(:)
    integer :: gridsize, x, y, z, c1, c2, total, s
    real :: pr, psize, dx, dy, dz, length, v, small
    logical :: cave
    
    side = 3.99676
    pr = 0.316563
    nuse = 2
    pnum = 2180
    na = 3
    psize = 0.15
    bin = 0.1
    nskip = 0
    cavbin = 0.01
    xtcfile = 'traj.xtc' 
    outfile = 'pdist.dat'
    print *, "Beginning formatting"

    gridsize = ceiling(side/bin)
    coordnum = 3 * na * pnum
    allocate(coord(coordnum))
    coord = 0
    total = gridsize**3 * nuse
    s = .5/cavbin
    allocate(results(s))
    nframe = 0
    open(unit = 10, file = outfile)
    call xdrfopen(uz, xtcfile, 'r', ret)
    results = 0
    if (ret == 1) then
        c1 = 0
            do while (ret == 1 .and. nframe < (nskip + nuse))
                    call readxtc(uz, natoms, istep, time, gbox, &
                    coord, prec, ret)
                    do i = 1, s
                        reff = i * cavbin
                        small = (i-1) * cavbin
                        do x = 1, gridsize
                            do y = 1, gridsize
                                do z = 1, gridsize
                                    cave = .TRUE.
                                    do k = 1, size(coord), 9
                                        dx = abs((x * bin) - coord(k))
                                        dy = abs((y * bin) - coord(k + 1))
                                        dz = abs((z * bin) - coord(k + 2))
                                        if (dx > 0.5 * side) dx = dx - side
                                        if (dy > 0.5 * side) dy = dy - side
                                        if (dz > 0.5 * side) dz = dz - side
                                        length = sqrt(dx**2 + dy**2 + dz**2)
                                        !if ((length < reff) .and. (length > small)) then
                                        if (length < reff) then
                                            !print *, length
                                            cave = .FALSE.
                                            exit
                                        end if
                                    end do
                                    if (cave) then 
                                        results(i) = results(i) + 1
                                    end if
                                end do
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
        results(i) = results(i) / (gridsize**3 * nuse)
        write(10,*) i*cavbin, results(i)
    end do

    write(*,*) ' '
    write(*,*) 'Done'
    write(*,*) ' '
    
end program data_format   
