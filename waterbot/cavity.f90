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
    
    side = 5
    pr = 0.316563
    nuse = 10
    pnum = 4142
    na = 3
    psize = 0.15
    bin = 0.1
    nskip = 0
    cavbin = 0.01
    xtcfile = 'ccni.xtc' 
    outfile = 'cav1.dat'
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
                    do x = 1, gridsize
                        do y = 1, gridsize
                            do z = 1, gridsize
                                cave = .TRUE.
                                small = 10
                                do k = 1, size(coord), 9
                                        dx = abs((x * bin) - coord(k))
                                        dy = abs((y * bin) - coord(k +1))
                                        dz = abs((z * bin) - coord(k +2))
                                        if (dx > 0.5 * side) dx = dx -side
                                        if (dy > 0.5 * side) dy = dy -side
                                        if (dz > 0.5 * side) dz = dz -side
                                        length = sqrt(dx**2 + dy**2 +dz**2)
                                        small = min(length, small)
                                end do
                                c2 = floor(small/cavbin) + 1
                                results(c2) = results(c2) + 1
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