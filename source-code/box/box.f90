! 0 is for Owen
! This file calculates and outputs the boxes of a certain simulation
! Splits it into to boxes and outputs the cavity size at the center of the box

program data_format
    implicit none
    integer :: nuse, nskip, narg, i, nframe, uz, ret, &
     natoms, istep, j, c, k, m, pnum, na, coordnum
    real :: time, gbox(3,3), prec, bin, ength, side, reff
    character (len = 256) :: fname, xtcfile, arg(50), outfile
    real, allocatable :: coord(:), boxes(:,:,:)
    integer :: gridsize, c1, c2, total, NUM, BOXNUM
    real :: x, y, z
    real :: pr, psize, dx, dy, dz, length, v, mid, temp, small
    logical :: cave
    real :: dist(20), points(83), center(3)

    side = 4 ! Side length of the box
    nuse = 100 ! Number of frames to use
    pnum = 2180 ! Nunber of particles
    na = 3
    nskip = 0
    xtcfile = 'traj.xtc' ! Input file
    outfile = 'btest1.dat' ! Output file
    print *, "Beginning formatting"
    reff = 0.25 ! Radius

	! Number of boxes to split the full box to be split into
    BOXNUM = 512
    coordnum = 3 * na * pnum
    allocate(coord(coordnum))
    coord = 0
    nframe = 0
    NUM = 84 ! Number of coordinates to keep track of
    allocate(boxes(nuse, BOXNUM, NUM+3)) ! The results 
    boxes = 0
    open(unit = 10, file = outfile)
    call xdrfopen(uz, xtcfile, 'r', ret)
    if (ret == 1) then
        c1 = 0
            do while (ret == 1 .and. nframe < (nskip + nuse))
                    call readxtc(uz, natoms, istep, time, gbox, &
                    coord, prec, ret)
					do k = 1, size(coord), 9
						! Go through every one of the coordinates and place it into a box
						! I don't think that this code is general enough to work for any box, I think that the
						! 64 should be changed
                        x = coord(k)
                        y = coord(k+1)
                        z = coord(k+2)
                        if (x >= 4) x = 3.999
                        if (y >= 4) y = 3.999
                        if (z >= 4) z = 3.999
                        total = floor(x/0.5)
                        total = 64*total
                        total = total + 8 * (floor(y/0.5))
                        total = total + floor(z/0.5) + 1
                        if (boxes(nframe+1, total, NUM) == 0) boxes(nframe+1, total, NUM) = 1
                        i = boxes(nframe+1, total, NUM)
						!print *, nframe+1, total, i
						! Error checking
                        if ((i > NUM-5) .or. (total < 1)) then 
                                print *, "ERROR HERE", nframe+1, total, i, x, y, z
                                continue
                        end if
                        boxes(nframe+1, total, i) = x
                        boxes(nframe+1, total, i+1) = y
                        boxes(nframe+1, total, i+2) = z
                        boxes(nframe+1, total, NUM) = boxes(nframe+1, total, NUM) + 3
                        !add center point to box, maybe shift all over 
                    end do
                    print *, nframe
                    nframe = nframe + 1
            end do
    else
            write(*,*) 'Error in the xdrfopen'
            stop
    end if
    c1 = 0
    c2 = 0
    print *, 'Out of main do'
    do i = 1, nuse
        do j = 1, BOXNUM
                ! I realize after writing this, that it would probably be easier to have
				! just used some modular math than this. 
				! This now calculates all the information about the box. For each box, it calculates and records
				! whether a cavity of a certain size exists and the size of the cavity at that point
                mid = floor(real(j-1)/64) + 1
                mid = mid * 0.5
                mid = mid - 0.25
                center(1) = mid
                mid = floor(real(j-1)/64) * 64
                mid = j - mid - 1
                mid = floor(mid/8) + 1
                mid = mid * 0.5
                mid = mid - 0.25
                center(2) = mid
                mid = floor(real(j-1)/64) * 64
                temp = j - mid - 1
                mid = floor(temp/8) * 8
                mid = temp - mid + 1
                mid = mid * 0.5
                mid = mid - 0.25
                center(3) = mid
                cave = .TRUE.
                small = 0.5
                ! do all nearby ones
                do k = 1, NUM-5, 3
                        if ((boxes(i, j, k) < 0.001) .and. (boxes(i, j, k+1) < 0.001) .and.(boxes(i, j, k+2) < 0.001)) cycle
                        !read(*,*)
                        dx = abs(center(1) - boxes(i, j, k))
                        dy = abs(center(2) - boxes(i, j, k+1))
                        dz = abs(center(3) - boxes(i, j, k+2))
                        length = sqrt(dx**2 + dy**2 + dz**2)
                        small = min(length, small)
                        if (length < reff) then 
                                cave = .FALSE.
                                exit
                        end if 
                end do
                !print *, small, "Number of times in loop", c1
                if (cave) then 
                        c2 = c2 + 1
                        boxes(i, j, NUM-2) = 1
                end if
                boxes(i, j, NUM-1) = small
                c1 = c1 + 1
                do k = 1, NUM-1
                        points(k) = boxes(i, j, k)
                end do
                boxes(i, j, 1) = center(1)
                boxes(i, j, 2) = center(2)
                boxes(i, j, 3) = center(3)
                do k = 1, NUM
                        boxes(i, j, k+3) = points(k)
                end do
                !do k = 1, NUM
        end do
    end do
     
    print *, "Number of cavities:", c2, real(c2)/c1, c1, BOXNUM*nuse

	! Writes the output to the file
    do i = 1, nuse
            do j = 1, BOXNUM
                do k = 1, NUM+2
                        write(10,"(F10.3)",advance='no') boxes(i, j, k)
                end do
                write(10,*)
            end do
    end do

    write(*,*) ' '
    write(*,*) 'Done'
    write(*,*) ' '
    
end program data_format  

