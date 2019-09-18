! 0 is for Owen
! This is an attempted at refactoring template.f (Camille) into a f90
! file

program diffusivity
        implicit none
        integer :: nuse, nskip, narg, i, nframe, ndone, uz, ret, &
         natoms, istep, j, c, k, v, pnum, maxbins
        real :: time, gbox(3,3), prec, bin, dx, dy, dz, length, &
         side, pi
        character (len = 256) :: fname, xtcfile, arg(50), outfile
        ! Variables for analysis
        real, allocatable :: rdf(:), coord(:), calcdist(:), rrdf(:)
        
        pi = 3.1415926
        bin = 0.01
        side = 5
        nuse = 10
        pnum = 12426
        nskip = 0 
        outfile = 'xtcoutput.dat'
        write(*,*) ' '
        write(*,*) 'Diffusivity calculation started!!'
        write(*,*) ' '   

        narg = iargc()
        do i = 1, narg
                call getarg(i, arg(i))
        end do        

        if (narg == 1) then
                write(*,*) 'Use flags -xtc -pdb -nskip -nuse'
                stop
        end if
        
        do i = 1, narg
                if(arg(i) == '-xtc') then
                        xtcfile = arg(i + 1)
                !else if arg(i) == '-pdb') then
                !        pdbfile = arg(i + 1)
                else if(arg(i) == '-bin') then
                        read(arg(i + 1),*) bin
                else if(arg(i) == '-o') then
                        outfile = arg(i + 1)
                else if(arg(i) == '-nskip') then
                        read(arg(i + 1),*) nskip
                else if(arg(i) == '-nuse') then
                        read(arg(i + 1),*) nuse
                else if(arg(i) == '-p') then
                        read(arg(i + 1),*) pnum
                else if(arg(i) == '-s') then
                        read(arg(i + 1),*) side
                end if
        end do
        
        pnum = pnum * 3
        length = side * 2
        maxbins = ceiling(length/bin)
        allocate(rdf(maxbins))
        rdf = 0 
        allocate(coord(pnum))
        nframe = 0
        ndone = 0
        open(unit = 10, file = outfile)
        call xdrfopen(uz, xtcfile, 'r', ret)
        if (ret == 1) then
                do while (ret == 1 .and. nframe < (nskip + nuse))
                        call readxtc(uz, natoms, istep, time, gbox, &
                        coord, prec, ret)
                        v = 0
                        do i = 1, size(coord)
                                if (coord(i) > 0) v = v + 1
                        end do
                       !print *, v
                        do i = 1, pnum, 9
                                if (allocated(calcdist)) deallocate(calcdist)
                                allocate(calcdist(pnum))
                                calcdist = 0
                                do k = i + 9, pnum, 9
                                        !print *, i, k
                                        dx = abs(coord(i) - coord(k))
                                        dy = abs(coord(i + 1) - coord(k + 1))
                                        dz = abs(coord(i + 2) - coord(k + 2))
                                        if (dx > 0.5 * side) dx = dx - side
                                        if (dy > 0.5 * side) dy = dy - side
                                        if (dz > 0.5 * side) dz = dz - side
                                        calcdist(k) = sqrt(dx**2+dy**2+dz**2)
                                        if (calcdist(k) < 0.2) then
                                               !print *, i, k, calcdist(k)
                                               !print *, dx, dy, dz
                                        end if
                                        !if (i == 19621) print *, calcdist(k), i , k        
                                end do
                                v = 0
                                do j = 1, size(calcdist)
                                        if (calcdist(j) == 0) cycle
                                        c = floor(calcdist(j) / bin) + 1
                                        rdf(c) = rdf(c) + 1
                                        v = v + 1
                                end do
                                !print *, i, v
                        end do
                        print *, nframe
                        nframe = nframe + 1
                        if (nframe > nskip .and. nframe < (nskip + nuse)) then
                                ndone = ndone + 1
                        end if
                end do
        else
                write(*,*) 'Error in the xdrfopen'
                stop
        end if
        allocate(rrdf(size(rdf)))
        print *, size(rdf), sum(rdf)
        do i = 1, size(rdf)
                rrdf(i) = rdf(i) / (sum(rdf) / (real(pnum) / 9.))
                rrdf(i) = real(rrdf(i)) / ((4./3. * pi * (((bin * real(i)) ** 3) - (bin * (real(i) - 1.)) ** 3)))
                rrdf(i) = rrdf(i) / ((pnum / 9.) / side ** 3)
        end do
        print *, nframe
        do i = 1, size(rdf)
                write(10,*) bin * i, rrdf(i), rdf(i)
        end do

        write(*,*) ' '
        write(*,*) 'Probability of binding calculation ended'
        write(*,*) ' '
        
end program diffusivity     
