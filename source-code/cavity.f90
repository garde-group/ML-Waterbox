! This program is generates the data for the nearest coordinate code
program data_format
    implicit none
    integer :: nuse, nskip, narg, i, nframe, uz, ret, &
     natoms, istep, j, c, k, m, pnum, na, coordnum
    real :: time, gbox(3,3), prec, bin, ength, side, reff
    character (len = 256) :: fname, xtcfile, arg(50), outfile
    real, allocatable :: coord(:), diff(:), up(:), results(:,:)
    integer :: gridsize, x, y, z, c1, c2, total
    real :: pr, psize, dx, dy, dz, length, v
    logical :: cave
    real :: dist(20), points(60)
    
    side = 3.99676 ! Box side length
    pr = 0.316563
    nuse = 10 ! Frames to use
    pnum = 2180 ! Number of water moleucles
    na = 3
    psize = 0.15 ! Particle size to be inserted
    bin = 0.1 ! Distance between gridpoints
    nskip = 0
    xtcfile = 'traj2.xtc' ! Input file
    outfile = 'coord.dat' ! Output file
    print *, "Beginning formatting"

    gridsize = ceiling(side/bin)
    coordnum = 3 * na * pnum
    allocate(coord(coordnum)) ! Allocating the input coordinates
    coord = 0
    total = gridsize**3 * nuse
    allocate(results(total, 64)) 
    nframe = 0
    open(unit = 10, file = outfile)
    print *, gridsize, total
    call xdrfopen(uz, xtcfile, 'r', ret)
    if (ret == 1) then
        c1 = 0
            do while (ret == 1 .and. nframe < (nskip + nuse))
                    call readxtc(uz, natoms, istep, time, gbox, &
                    coord, prec, ret)
                    reff = (real(psize + pr)) / 2 ! Effective radius
                    do x = 1, gridsize  
                        do y = 1, gridsize
                                do z = 1, gridsize ! Iteratre through the grid
                                        c1 = c1 + 1
                                        results(c1, 1) = (x*bin)
                                        results(c1, 2) = (y*bin) 
                                        results(c1, 3) = (z*bin)
                                        cave = .TRUE.
                                        points = 0 ! Keeps track of the nearest points
                                        dist = 10 ! Keeps track of the nearest distances
                                        do k = 1, size(coord), 9 ! Go through the coordinates to find the nearest 20
                                                dx = abs((x * bin) - coord(k))
                                                dy = abs((y * bin) - coord(k + 1))
                                                dz = abs((z * bin) - coord(k + 2))
                                                if (dx > 0.5 * side) dx = dx - side
                                                if (dy > 0.5 * side) dy = dy - side
                                                if (dz > 0.5 * side) dz = dz - side
                                                length = sqrt(dx**2 + dy**2 + dz**2)
                                                ! If one of the nearest waters so far, record the distances and the coordinates for future reference
                                                if(length < maxval(dist)) then
                                                        c2 = (maxloc(dist, DIM=1) - 1) * 3 + 1
                                                        dist(maxloc(dist)) = length
                                                        points(c2) = coord(k)
                                                        points(c2+1) = coord(k+1)
                                                        points(c2+2) = coord(k+2)
                                                end if
                                                ! If there is no cavity at the given size, then set it to false
                                                if (length < reff) then
                                                        cave = .FALSE.
                                                end if
                                        end do
                                        ! Copy over the points into the results array 
                                        do k = 1, size(points)
                                                results(c1, k+3) = points(k)
                                        end do
                                        ! Record if there is a cavity
                                        if (cave) then
                                                results(c1, 64) = 1
                                        else 
                                                results(c1, 64) = 0
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

    ! Write the output to the output file
    do i = 1, total
            write(10,"(F10.3)",advance='no') results(i, 1)
            do j = 2, 64
                write(10,"(F10.3)",advance='no') results(i, j)
            end do
            write(10,*)
    end do

    write(*,*) ' '
    write(*,*) 'Done'
    write(*,*) ' '
    
end program data_format   
